// A fork of https://github.com/sssvip/simple-file-server
// Erfan Namira
// https://github.com/ErfanNamira/AriaFileServer

package main

import (
	"fmt"
	"path/filepath"
	"os"
	"log"
	"strings"
	"io/ioutil"
	"net/http"
	"strconv"
	"net"
	"encoding/base64"
	"time"
	"github.com/sssvip/qrterminal"
)

var staticPath = "/static/"
var repoUrl = "https://github.com/ErfanNamira/AriaFileServer"

var (
	// Define a map to store username-password pairs
	userDB = map[string]string{
		"username": "password", // Replace with your desired username and password
	}

	// Configuration options
	config = struct {
		Port               string
		EnableHTTPS        bool
		EnableDirectoryListing bool
	}{
		Port:               "80",
		EnableHTTPS:        false, // Change to true to enable HTTPS
		EnableDirectoryListing: true, // Change to false to disable directory listing
	}
)

func listDir(dirPth string) (a []string) {
	dir, err := ioutil.ReadDir(dirPth)
	if err != nil {
		log.Println("Error reading directory:", err)
		return nil
	}
	var files []string
	for _, fi := range dir {
		files = append(files, fi.Name())
	}
	// Sort files alphabetically
	sortStringSlice(files)
	return files
}

func sortStringSlice(slice []string) {
	sort.Slice(slice, func(i, j int) bool {
		return strings.ToLower(slice[i]) < strings.ToLower(slice[j])
	})
}

func getCurrentDirectory() string {
	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		log.Fatal("Error getting current directory:", err)
	}
	return dir
}

func home(w http.ResponseWriter, r *http.Request) {
	user, pass, _ := r.BasicAuth()
	if isValidUser(user, pass) {
		currentPath := getCurrentDirectory()
		fmt.Fprintf(w, "<h1>Files in [%s]</h1></br></br></br>", currentPath)
		fileNames := listDir(currentPath)
		if config.EnableDirectoryListing {
			renderDirectoryListing(w, fileNames)
		} else {
			fmt.Fprintln(w, "<p>Directory listing is disabled.</p>")
		}
		fmt.Fprintf(w, "</br></br></br>See the new version of AriaFileServer :<a href=\"%s\">%s</a>", repoUrl, repoUrl)
	} else {
		w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
		http.Error(w, "Unauthorized access", http.StatusUnauthorized)
		log.Printf("Unauthorized access from %s", r.RemoteAddr)
	}
}

func isValidUser(username, password string) bool {
	storedPassword, ok := userDB[username]
	return ok && password == storedPassword
}

func getLocalIPs() []string {
	result := []string{"localhost"}
	addrSlice, err := net.InterfaceAddrs()
	if err != nil {
		log.Println("Error getting local IP addresses:", err)
		return result
	}
	for _, addr := range addrSlice {
		if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				result = append(result, ipnet.IP.String())
			}
		}
	}
	return result
}

func entry() {
	port := config.Port
	showQRCode := false
	const qr = "qr"
	showQRCodeIpFilter := qr

	if len(os.Args) > 1 {
		tmpPort, err := strconv.Atoi(os.Args[1])
		if err != nil {
			log.Println("HTTP port must be a number, e.g., AriaFileServer.exe 8080")
			log.Println("Using default HTTP port:" + port)
		} else {
			port = strconv.Itoa(tmpPort)
		}
		// Check for QR code generation
		for _, arg := range os.Args {
			if strings.Contains(arg, qr) {
				showQRCode = true
				showQRCodeIpFilter = arg
				break
			}
		}
	}

	http.HandleFunc("/", home)
	http.HandleFunc(staticPath, func(w http.ResponseWriter, r *http.Request) {
		log.Println(r.RemoteAddr, "=>", r.URL.Path)
		// Implement caching with a one-hour expiration time
		expires := time.Now().Add(time.Hour)
		w.Header().Set("Cache-Control", "public, max-age=3600")
		http.ServeFile(w, r, r.URL.Path[len(staticPath):])
	})

	startEcho := "started file server http://127.0.0.1"
	if port != "80" {
		startEcho = fmt.Sprintf("%s:%s", startEcho, port)
	}
	log.Println(startEcho)

	optPreAddr := "Optional addr: "
	for _, localIP := range getLocalIPs() {
		urlAddr := fmt.Sprintf("http://%s", localIP)
		if port != "80" {
			urlAddr = fmt.Sprintf("%s:%s", urlAddr, port)
		}
		log.Println(fmt.Sprintf("%s%s", optPreAddr, urlAddr))
		if showQRCode {
			if showQRCodeIpFilter != qr {
				if strings.Contains(urlAddr, strings.Replace(showQRCodeIpFilter, qr, "", -1)) {
					qrterminal.Generate(urlAddr, qrterminal.L, os.Stdout)
					fmt.Println()
					break
				}
			} else {
				qrterminal.Generate(urlAddr, qrterminal.L, os.Stdout)
				fmt.Println()
			}
		}
	}

	var serverAddr string
	if config.EnableHTTPS {
		serverAddr = ":" + port
		go func() {
			log.Fatal(http.ListenAndServeTLS(serverAddr, "cert.pem", "key.pem", nil))
		}()
		log.Printf("HTTPS server started at https://127.0.0.1:%s", port)
	} else {
		serverAddr = ":" + port
		go func() {
			log.Fatal(http.ListenAndServe(serverAddr, nil))
		}()
		log.Printf("HTTP server started at http://127.0.0.1:%s", port)
	}

	// Graceful shutdown with Ctrl+C
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)
	<-interrupt
	log.Println("Shutting down...")
}

func main() {
	entry()
}

func renderDirectoryListing(w http.ResponseWriter, fileNames []string) {
	tmpl := `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Directory Listing</title>
	<style>
		body {
			font-family: Arial, sans-serif;
			margin: 20px;
		}
		h2 {
			margin-bottom: 10px;
		}
		ul {
			list-style-type: none;
			padding: 0;
		}
		li {
			margin-bottom: 5px;
		}
	</style>
</head>
<body>
	<h2>Directory Listing</h2>
	<ul>
		{{range .}}
			<li><a href="{{$.}}{{.}}">{{.}}</a></li>
		{{end}}
	</ul>
</body>
</html>`
	tmpl = strings.Replace(tmpl, "{{.}}", staticPath, -1)
	t := template.Must(template.New("listing").Parse(tmpl))
	err := t.Execute(w, fileNames)
	if err != nil {
		http.Error(w, "Failed to render directory listing", http.StatusInternalServerError)
		log.Println("Error rendering directory listing:", err)
	}
}
