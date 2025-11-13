const toggleButton = document.getElementById('toggle-btn')
const sidebar = document.getElementById('sidebar')

function toggleSidebar(){
    sidebar.classList.toggle('close')
    toggleButton.classList.toggle('rotate')
    closeAllSubMenus()
}

function toggleSubMenu(button){

    if(!button.nextElementSibling.classList.contains('show')){
        closeAllSubMenus()
    }
    button.nextElementSibling.classList.toggle('show')
    button.classList.toggle('rotate')

    if(sidebar.classList.contains('close')){
        sidebar.classList.toggle('close')
        toggleButton.classList.toggle('rotate')
    }
}


function closeAllSubMenus(){
        Array.from(sidebar.getElementsByClassName('show')).forEach(ul =>{
        ul.classList.remove('show')
        ul.previousElementSibling.classList.remove('rotate')
    })
}

async function submitPrompt(event){
    event.preventDefault();  // STOP the normal form submission
    const promptInput = document.getElementById('prompt').value;
    const model = document.getElementById('model').value;
    
    const res = await fetch('https://api.jaredwjbrown.com/api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptInput, model: model })
    })
    showLoader();






    const data = await res.json();
    const jobId = data.job_id;

    // Poll for JSON result
    let status = "pending";
    while (status !== "done") {
        await new Promise(r => setTimeout(r, 10000));
        const sres = await fetch(`https://api.jaredwjbrown.com/api/result/${jobId}`);
        const sdata = await sres.json();
        status = sdata.status;
        if (status === "done") {
          try{
            const result = sdata.result; // This is your dictionary from run_wala
            console.log("JSON result ready:", result);
            // You can trigger the download using your existing code
            const base64String = result.data;
            const binaryString = atob(base64String);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }
            console.log("Len = " + len)
            // Create a Blob and trigger download
            const blob = new Blob([bytes], { type: "text/plain" });
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = data.filename || "model.obj"; // use filename from server if available
            document.body.appendChild(a);
            a.click();

            // Cleanup
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          }
          catch(err) {
        console.error("Error fetching or downloading OBJ:", err);
        };
       }
      }
      hideLoader();
}




function showLoader() {
    document.getElementById("loader").style.display = "block";
}

function hideLoader() {
    document.getElementById("loader").style.display = "none";
}