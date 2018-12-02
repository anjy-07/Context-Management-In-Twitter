// setup some JSON to use
var userN = [
	{ "name":"Shivangi31172"}
];

window.onload = function() {
	// setup the button click
	document.getElementById("theButton").onclick = function() {		
      document.getElementById("time").innerHTML = "Average time to compute the Algorithim is 15-20 mins. Please wait";
		userN[0].name= document.getElementById("name").textContent;
		doWork()
	};
}

var getHTML = function ( url, callback ) {

	// Feature detection
	if ( !window.XMLHttpRequest ) return;

	// Create new request
	var xhr = new XMLHttpRequest();

	// Setup callback
//	xhr.onload = function() {
	//	if ( callback && typeof( callback ) === 'function' ) {
		//	callback( this.responseXML );
		//}
	//}

	// Get the HTML
	xhr.open( 'GET', url );	
	xhr.responseType = 'document';
	xhr.send();

};

function myFunction(arr) 
{  
	   var i;
	   var txt = "<table>";
	for(i=0;i<3;i++)
	{
		txt+="<tr>";
       for (x in arr.list1) 
	   {
            txt += "<td width='33%'> <div class='card'><img src='https://avatars.io/twitter/" + arr.list1[x].user + "' alt='Avatar' style='width:80px;height:80px'>";
	        txt += " <div class='container'><h4><b>"+ arr.list1[x].user + "</b></h4> <a href='https://twitter.com/" +arr.list1[x].user + "'  class='btn btn-primary btn-xs'style='padding-right:2px'>Unfollow</a></div> </div>";
            txt += "</td></tr>";
        }
	   txt+="</tr>";
	}
        txt += "</table>" ;
        document.getElementById("followeeList").innerHTML = txt;
}

function doWork() {
	// ajax the JSON to the server
	var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
		
        var myArr = JSON.parse(this.responseText);
		document.getElementById("time").style.display="none";
        myFunction(myArr);
		
      //document.getElementById("Analysis").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "http://localhost:5000/receiver", true);
  xhttp.send(JSON.stringify(userN));
	// stop link reloading the page
 event.preventDefault();
}