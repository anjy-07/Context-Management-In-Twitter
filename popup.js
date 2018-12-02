// Update the relevant fields with the new data
function setDOMInfo(info) {
  document.getElementById('name').innerHTML   = info.name;
  document.getElementById('id_python').textContent  = info.id_python;
 // document.getElementById('pic_url').textContent = info.pic;
  //document.getElementById('pic').src = info.pic;
}

// Once the DOM is ready...
window.addEventListener('DOMContentLoaded', function () {
  // ...query for the active tab...
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, function (tabs) {
    // ...and send a request for the DOM info...
    chrome.tabs.sendMessage(
        tabs[0].id,
        {from: 'popup', subject: 'DOMInfo'},
        // ...also specifying a callback to be called 
        //    from the receiving end (content script)
        setDOMInfo);
  });
});