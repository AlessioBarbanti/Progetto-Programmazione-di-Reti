import sys, signal
import http.server
import socketserver
import cgi

port = 8080
ownLocalIPAdress = "192.168.178.38"
allowedIPAddress = []

html ="""
    <html>
        <body>
        		<form action="http://{ownLocalIPAdress}:{port}/?Registrati" method="post">
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
        		<form action="http://{ownLocalIPAdress}:{port}/?Login" method="post"> <h1><strong> LOGIN </strong></h1><br>
        		  <label for="name">NOME UTENTE:</label><br>
        		  <input type="text" id="name" name="name"><br>
        		  <label for="passw">PASSWORD:</label><br>
                  <input type="text" id="passw" name="passw"><br>
              <input type="hidden" value="true">
              <input type="submit">
        
        		</form>
           <br>     
           <a href="{ownLocalIPAdress}:{port}/traccia.pdf" download="traccia2 esame 2021.pdf" >Scarica Traccia</a>
        </body>
    </html>
    """.format(port=port, ownLocalIPAdress = ownLocalIPAdress)






class MyHandler(http.server.SimpleHTTPRequestHandler):
    
    
            
    def do_POST(self):
            # print("CLIENT ADDRESS: ", self.client_address[0])
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            name = form.getvalue('name')
            passw = form.getvalue('passw')

 
            if self.path.find("Registrati") != -1:               
                if check_existing_name(name) == -1 or check_existing_name(name) == None:
                    with open("Account.txt", "a") as account_list:
                        data = name + "-" + passw +"\n"
                        account_list.write(data)       
                    print("Successfull Registration")

                else:
                    print("Account already existing")

                
            if self.path.find("Login") != -1:
                if check_credentials(name, passw) == 1:
                    print("Successful Login ")
                    global allowedIPAddress
                    if self.client_address[0] not in allowedIPAddress:
                        allowedIPAddress.append(self.client_address[0])
                        print(allowedIPAddress)
                        self.send_response(302)
                        self.send_header('Location','/servizio.html')
                    
                else:
                    print("Failed Login ")

            self.do_GET()
            
    def do_GET(self):
        if self.client_address[0] in allowedIPAddress:
            if self.path.find("servizio") == -1:
                self.send_response(302)
                self.send_header('Location','/servizio.html')
        else:
            if self.path.find("servizio") != -1:
                self.send_response(302)
                self.send_header('Location','/index.html')

        
        http.server.SimpleHTTPRequestHandler.do_GET(self)

      
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
            
def print_pages():
            f = open('index.html','w', encoding="utf-8")
            f.write(html)
            f.close()
    

server = socketserver.ThreadingTCPServer((ownLocalIPAdress,port), MyHandler)


def signal_handler(signal, frame):
    print("Spegnimento del Server")
    try:
      if(server):
        server.server_close()
    finally:
      sys.exit(0)
      
def main():
    server.daemon_threads = True 
    signal.signal(signal.SIGINT, signal_handler)

    
    # DEBUG cancella i dati account ogni volta che il server viene attivato
    print_pages()
    f = open('Account.txt','w', encoding="utf-8")
    f.close()
    

    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
    main()
