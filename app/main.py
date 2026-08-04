from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from app.methods import get_client_ip, save_hostname_ip, get_ip_by_hostname, TTL

app = FastAPI(title="Sber Test")


@app.get("/")
async def root(request: Request, hostname: str = Query(None)):

    client_ip = get_client_ip(request)

    if hostname:
        save_hostname_ip(hostname.strip(), client_ip)
        return {
            "ip": client_ip,
            "hostname": hostname,
            "status": "saved",
            "ttl_seconds": TTL,
        }

    return {"ip": client_ip}


@app.get("/lookup/{hostname}")
async def lookup(hostname: str):
    ip = get_ip_by_hostname(hostname)
    if ip:
        return {"hostname": hostname, "ip": ip}
    return JSONResponse(
        status_code=404,
        content={"error": "hostname not found"}
    )
