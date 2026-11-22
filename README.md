# BSDK Clube - Webpage & APK Distribution

A super-fast, responsive, and lightweight landing page allowing users to download your **BSDK Clube** app and enabling you to upload new updates.

---

## 📁 Files
1. `index.html` - Fast main landing page (responsive, modern dark theme, instant download button).
2. `server.py` - Lightweight Python backend to upload new `.apk` files directly from your browser using password protection.
3. `config.json` - Stores current version, file size, and download link.

---

## 🚀 How to Run & Test (Locally / Wi-Fi)

1. Open your terminal and navigate to this folder:
   ```bash
   cd C:\Users\PIYUSH\.gemini\antigravity\scratch\bsdk-clube-web
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Open in your browser:
   👉 **http://localhost:8080**
4. **To test on a mobile device:**
   Find your PC's Wi-Fi IP address (for example, `http://192.168.1.5:8080`) and open it in your phone's browser!

---

## 👑 How to Upload & Update (Owner Guide)

1. Click the **"Owner Login"** button in the top-right corner of the website.
2. Enter the secret password:
   - **Password:** 
3. You have two options:
   - **Direct File Upload:** Select a new `.apk` file, enter the version number, and click "Upload & Update APK". The file updates immediately!
   - **Custom Link Update:** If you host your APK on Google Drive, Mediafire, or any cloud storage, enter the direct download link and save.

---

## 🌐 How to Host Online for Free (GitHub / Netlify)

If you want to make this website accessible to everyone on the internet:
1. **GitHub Pages (100% Free):**
   - Create a repository on GitHub.
   - Upload `index.html` and your `bsdk-clube.apk` file.
   - Go to Settings -> Pages and enable "Deploy from Branch".
   - Your website will be live (e.g., `https://yourname.github.io/bsdk-clube`).
2. **Netlify / Vercel (Drag & Drop):**
   - Drag and drop the `bsdk-clube-web` folder into Netlify to go live in seconds.
