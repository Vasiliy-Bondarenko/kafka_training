# Events tunnel

## How to use it
Enter random ETH_GATEWAY_EVENTS_ENDPOINT_TUNNEL_DOMAIN in your .env file.  

After starting `eth_gateway_tunnel` docker service you can look it's logs to see it's running `docker-compose logs eth_gateway_tunnel` - you should see something like 
```
eth_gateway_tunnel_1   | your url is: https://eth-gateway-XXXXXXXXXX.loca.lt
```
This is you tunnel url. Tunnel allows to send events to real URL on the internet and these calls will be forwarded to your local environment. In particular this tunnel will forward calls to `eth_gateway_events` host on port `6066` - this is where endpoint is actually hosted. 
Events will be received on `/events/` endpoint.  
Your webhook full url will look like `https://${ETH_GATEWAY_EVENTS_ENDPOINT_TUNNEL_DOMAIN}.loca.lt/events/`
