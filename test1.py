
import sys, signal
import http.server
import socketserver
import socket
import cgi


html ="""
        <html>
            <head>
                <style>
                
                
        #servizi {
          font-family: Arial, Helvetica, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }
        
        #servizi td, #servizi th {
          border: 1px solid #ddd;
          padding: 8px;
        }
        
        #servizi tr:nth-child(even){background-color: #f2f2f2;}
        
        #servizi tr:hover {background-color: #ddd;}
        
        #servizi th {
          padding-top: 12px;
          padding-bottom: 12px;
          text-align: left;
          background-color: #04AA6D;
          color: white;
        }
        </style>
            </head>
            <body>
                <table id="servizi">
          <tr>
            <th>Servizi</th>
          </tr>
          <tr>
            <td><a href="Servizio 1.html">Servizio 1</a></td>
          </tr>
            <tr>
            <td><a href="Servizio 2.html">Servizio 2</a></td>
          </tr>
            <tr>
            <td><a href="Servizio 3.html">Servizio 3</a></td>
          </tr>
            <tr>
            <td><a href="Servizio 4.html">Servizio 4</a></td>
          </tr>
        </table>
        <br><br>
		<form action="http://6cfa93bda189.ngrok.io/?Registrati" method="post">
		  <h1><strong>REGISTRATI </strong></h1><br>
		  <label for="name">NOME UTENTE:</label><br>
		  <input type="text" id="name" name="name"><br>
		  <label for="passw">PASSWORD:</label><br>
          <input type="text" id="passw" name="passw"><br>
      <input type="hidden" value="true">
      <input type="submit">
		</form>        
        
        <br>       
        <br>
		<form action="http://6cfa93bda189.ngrok.io/?Login" method="post"> <h1><strong> LOGIN </strong></h1><br>
		  <label for="name">NOME UTENTE:</label><br>
		  <input type="text" id="name" name="name"><br>
		  <label for="passw">PASSWORD:</label><br>
          <input type="text" id="passw" name="passw"><br>
      <input type="hidden" value="true">
      <input type="submit">

		</form>
   <br>     
   <a href="http://1http://6cfa93bda189.ngrok.io/traccia.pdf" download="traccia2 esame 2021.pdf" >Scarica Traccia</a>
</body>
</html>
"""










class ServerHandler(http.server.SimpleHTTPRequestHandler):
    

            
    def do_POST(self):
            print("Client Address: ", socket.getfqdn())
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            name = form.getvalue('name')
            passw = form.getvalue('passw')

 
            if self.path.find("Registrati") != -1:               
                if check_existing_name(name) == -1 or check_existing_name(name) == None:
                    with open("Account.txt", "a") as account_list:
                        data = name + "-" + passw +"\n"
                        account_list.write(data)       
                    print("Registrazione effettuata con successo")
                else:
                    print("Account già esistente")
                
            if self.path.find("Login") != -1:
                if check_credentials(name, passw) == 1:
                    print("Successful Login ")
                else:
                    print("Failed Login ")
                

            self.do_GET()
          
def check_credentials(name, passw):
        for line in open("Account.txt","r").readlines():
            account_data = line.split("-")
            if name == account_data[0] and (passw + "\n") == account_data[1]:
                return 1
            else:
                return -1       
          

          
def check_existing_name(name):
         for line in open("Account.txt","r").readlines():
             account_data = line.split("-")
             
             if name == account_data[0]:
                 return 1
             else:
                 return -1      
            
def print_page():
            f = open('index.html','w', encoding="utf-8")
            f.write(html)
            f.close()
    

server = socketserver.ThreadingTCPServer(('127.0.0.1',8080), ServerHandler)


def signal_handler(signal, frame):
    print("interruzione")
    try:
      if(server):
        server.server_close()
    finally:
      sys.exit(0)
      
def main():
    server.daemon_threads = True 
    signal.signal(signal.SIGINT, signal_handler)

    
    # DEBUG cancella i dati account ogni volta che il server viene attivato
    print_page()
    f = open('Account.txt','w', encoding="utf-8")
    f.close()
    

    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
    main()
