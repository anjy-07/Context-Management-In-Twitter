// Inform the background page that 
// this tab should have a page-action
chrome.runtime.sendMessage({
  from:    'content',
  subject: 'showPageAction'
});

// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function (msg, sender, response) {
  // First, validate the message's structure
  if ((msg.from === 'popup') && (msg.subject === 'DOMInfo')) {
    // Collect the necessary data 
    // (For your specific requirements `document.querySelectorAll(...)`
    //  should be equivalent to jquery's `$(...)`)
    var domInfo = {
      name:   document.querySelector('#page-container > div.AppContainer > div > div > div.Grid-cell.u-size1of3.u-lg-size1of4 > div > div > div > div.ProfileHeaderCard > h1 > a').getAttribute("href"),
      id_python: document.querySelector('#page-container > div.AppContainer > div > div > div.Grid-cell.u-size1of3.u-lg-size1of4 > div > div > div > div.ProfileHeaderCard > h1 > a').textContent,
      pic: document.querySelector('#page-container > div.ProfileCanopy.ProfileCanopy--withNav.js-variableHeightTopBar > div > div.ProfileCanopy-header.u-bgUserColor > div.AppContainer > div.ProfileCanopy-avatar > div.ProfileAvatar > a.ProfileAvatar-container.u-block.js-tooltip.profile-picture > img').getAttribute("src")
    };

    // Directly respond to the sender (popup), 
    // through the specified callback */
    response(domInfo);
  }
});