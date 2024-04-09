package main

import (
	"bufio"
	"crypto/md5"
	"crypto/sha1"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"

	"github.com/cheggaaa/pb/v3"
)

func calculateHashes(filePath string) (string, string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", "", err
	}
	defer file.Close()

	sha1Hash := sha1.New()
	md5Hash := md5.New()

	if _, err := io.CopyBuffer(sha1Hash, file, nil); err != nil {
		return "", "", err
	}

	// Reset file pointer before calculating MD5 hash
	if _, err := file.Seek(0, io.SeekStart); err != nil {
		return "", "", err
	}

	if _, err := io.CopyBuffer(md5Hash, file, nil); err != nil {
		return "", "", err
	}

	return fmt.Sprintf("%x", sha1Hash.Sum(nil)), fmt.Sprintf("%x", md5Hash.Sum(nil)), nil
}

func getFileInfo(filePath string) (string, string, int64, string, string, error) {
	fileInfo, err := os.Stat(filePath)
	if err != nil {
		return "", "", 0, "", "", err
	}

	fileName := filepath.Base(filePath)
	fileSize := fileInfo.Size()
	fileExtension := filepath.Ext(fileName)
	createdDate := fileInfo.ModTime().Format("2024-04-09 15:04:05")

	return fileName, filePath, fileSize, fileExtension, createdDate, nil
}

func main() {
	var rootFolder string

	if len(os.Args) > 1 {
		// If command-line argument is provided, use it as root folder
		rootFolder = os.Args[1]
	} else {
		// If no command-line argument is provided, prompt user to enter root folder
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Enter the folder path: ")
		rootFolder, _ = reader.ReadString('\n')
		rootFolder = strings.TrimSpace(rootFolder)
	}

	outputCSV, err := os.Create(filepath.Join(rootFolder, "checksumsha1.csv"))
	if err != nil {
		fmt.Println("Error creating output CSV file:", err)
		return
	}
	defer outputCSV.Close()

	writer := csv.NewWriter(outputCSV)
	defer writer.Flush()

	err = writer.Write([]string{"Filename", "File Path", "SHA1 Hash", "MD5 Hash", "File Size", "File Extension", "Created Date"})
	if err != nil {
		fmt.Println("Error writing CSV header:", err)
		return
	}

	files := make([]string, 0)
	err = filepath.Walk(rootFolder, func(filePath string, fileInfo os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !fileInfo.IsDir() {
			files = append(files, filePath)
		}
		return nil
	})

	if err != nil {
		fmt.Println("Error, no folder path was entered.", err)
		return
	}

	bar := pb.StartNew(len(files))
	bar.Set(pb.Bytes, true)
	bar.SetTemplateString(`Processing digital objects and currently at the following percent: {{percent . }}`)

	for _, filePath := range files {
		sha1Hash, md5Hash, err := calculateHashes(filePath)
		if err != nil {
			fmt.Println("Error calculating hashes:", err)
			return
		}
		fileName, filePath, fileSize, fileExtension, createdDate, err := getFileInfo(filePath)
		if err != nil {
			fmt.Println("Error getting file info:", err)
			return
		}
		err = writer.Write([]string{fileName, filePath, sha1Hash, md5Hash, fmt.Sprint(fileSize), fileExtension, createdDate})
		if err != nil {
			fmt.Println("Error writing to CSV:", err)
			return
		}
		bar.Increment()
	}
	bar.Finish()
	fmt.Println("Checksums and file information are stored in the folder where the program was run.")
}
