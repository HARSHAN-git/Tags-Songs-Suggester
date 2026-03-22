console.log("Tags-Songs-Suggester content script loaded");
document.addEventListener(
  "change",                       //the eventlistener responds to any change event 
  //handler code
  async (e) => {
    const target = e.target;                          //the image is the object here
    if (target && target.type === "file") {
      const file = target.files[0];
      if (!file) return;
      console.log("📸 Image selected:", file.name);  
      const reader = new FileReader();               //creating a file reader object to read the input image
      reader.onload = async () => {
        try {
          const base64Image = reader.result;
          console.log("Sending to backend...");
          const res = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: base64Image }),
          });
          const responseData = await res.json();
          console.log("Response:", responseData);
          // SAFE STORAGE ACCESS
          if (chrome && chrome.storage && chrome.storage.local) {
            chrome.storage.local.set({
              tags: responseData.tags || [],
              songs: responseData.songs || []
            });
          } else {
            console.log("chrome.storage not available");
          }
        } catch (err) {
          console.error("❌ Error:", err);
        }
      };
      reader.readAsDataURL(file);
    }
  },
  true
);