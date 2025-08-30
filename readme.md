cloudflared login
	# select domain
cloudflared tunnel create sgi-api-tunnel
nano ~/.cloudflared/config_api.yml

	tunnel: sgi-api-tunnel
	credentials-file: /etc/cloudflared/file_name.json
	origincert: /etc/cloudflared/cert.pem

	ingress:
	  - hostname: apipost.huzaifa.cloud
	    service: http://localhost:4165
	  - hostname: apiget.huzaifa.cloud
	    service: http://localhost:1598
	  - service: http_status:404

cloudflared tunnel route dns sgi-api-tunnel apipost.huzaifa.cloud
cloudflared tunnel route dns sgi-api-tunnel apiget.huzaifa.cloud

sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/*.yml /etc/cloudflared/
sudo cp ~/.cloudflared/*.json /etc/cloudflared/
sudo cp ~/.cloudflared/*.pem /etc/cloudflared/

sudo cp /home/coder/Desktop/securegenai/server_api/main-central-api-server.service /etc/systemd/system/main-central-api-server.service

sudo cp /home/coder/Desktop/securegenai/server_api/cloudflared-api.service /etc/systemd/system/cloudflared-api.service

sudo /bin/systemctl daemon-reload
sudo /bin/systemctl daemon-reexec

sudo /bin/systemctl enable main-central-api-server
sudo /bin/systemctl start main-central-api-server

sudo /bin/systemctl enable cloudflared-api
sudo /bin/systemctl start cloudflared-api

----------------------------------------------------------------------------------
cloudflared tunnel --config ~/.cloudflared/config_api.yml run