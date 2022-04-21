# A new FortiSIEM Incident Remediation method based on a custom publishing script leveraging FortiGate Security Fabric External Connectors and/or 3rd party NGFW Connectors
<html>
<body>
<p>FortiSIEM is a highly flexible solution providing a wide collection of inbuilt Remediation Scripts, integrating FortiSOAR Playbooks or giving the user the ability to create his own custom remediation scripts.
</p>
<p>Predefined and custom FortiSIEM scripts can be invoked on-demand (manually) or automatically when the incident happens. A common situation for using remediation scripts includes blocking sources and/or destinations IP address for reported attacks or suspicious activities (ex. port scanning activities, communication with a C&C server, botnets, etc.).
</p>
<p> 
<img src="https://user-images.githubusercontent.com/66027832/164473427-b0a2a794-ecec-4d5c-83dd-909009a1ae5e.png" alt="001">
</p>
  
<p> 
These situations can also be addressed in an easy and reliable way by using a new remediation method based on a FortiSIEM publishing script leveraging Fortinet Security Fabric External Connectors and/or 3rd party NGFW Connectors. 
</p>  
<p> 
<img src="https://user-images.githubusercontent.com/66027832/164474348-55ccaa09-2165-404d-a821-7b42a67109a5.png">
</p>  

<h1> Video Presentation & Demo</h1>  
<p> 
<table>
<thead>
</thead>
<tbody>
<tr>
<td><a href="https://www.youtube.com/watch?v=ix6a1gvEowA" target="_blank" rel="nofollow"><img src="https://user-images.githubusercontent.com/66027832/164478736-303ba920-a4b0-41a5-bdd4-acb45536a9fd.JPG" alt="FortiSIEM remediation using External Connectors" data-canonical-src="ttps://img.youtube.com/vi/ix6a1gvEowA/0.jpg" style="max-width: 100%;"></a></td>
</tr>
 <tr>
<td><a href="https://www.youtube.com/watch?v=ix6a1gvEowA" rel="nofollow">Video Presentation & Demo</a></td>   
 </tr>
</tbody>
</table>
</p>  

<h1>Main advantages of this method:</h1>  
<table>
<thead>
</thead>
<tbody>
<p>
    •	One single publishing script can be used to integrate multiple and different FGT FOS versions and/or 3rd party firewall devices
</p>
<p>  
  •	Sources and/or Destinations IP address can be extracted from FortiSIEM Incident XML file and published in a HTML/txt file format in order to be easily fetched by Firewalls and used in specific policy rules
</p>
  <p>
  •	In case of a firewall firmware upgrade or configuration change, there is no need to update the FortiSIEM script  
</p>
  <p>
  •	Less computing resources needed, as there is no need to initiate and handle SSH sessions with each specific FortiGate or 3rd party Firewall
<p>
  <tp>
  •	Fast and easy deployment within Fortinet environment by copying the script on FortiSIEM Supervisor and using FortiManager to configure FortiGate Security Fabric External Connectors
<p>
  <p> 
  •	Sources or Destinations IP address can be fetched from FortiSIEM incidents and used by Firewalls to enforce different policy rules (with block or allow actions)
<p>
  <p>
  •	This method might be extended to use Hash and URL lists (not just IP address lists)
</p>
</tbody>
</table> 
</p>  

    
  <h1>Implementation & Testing</h1> 
<p>
   Details regarding implementation and testing procedures are available on this <a href="https://fusecommunity.fortinet.com/blogs/silviu/2022/04/12/fortisiempublishingscript"> Blog Article </a>  	 </p>
 </body>
</html>

