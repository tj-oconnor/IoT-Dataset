devices = [ {
                "name": "smartthings-motion-01",
                "uuid": "2cd8fe51-6b2e-4b3b-b590-f9d5b8334b95"
            },
            {
                "name": "smartthings-cam-01",
                "uuid": "2e3dc5e1-1e5d-4f3c-8766-009223c6fbd3"
            },
            {
                "name": "kwikset-lock-01",
                "uuid": "b1a0a0b2-99de-4e07-a4d3-8398083db551"
            },
            {
                "name": "smartthings-outlet-01",
                "uuid": "41b18556-d390-4856-90bc-a84cd7e6ec29"
            },
            {
                "name": "smartthings-water-01",
                "uuid": "95b83b2e-cd43-4ffd-9412-7fda6079f226"
            },
            {
                "name": "yale-lock-01",
                "uuid": "79eff5e9-4718-41fa-8d3f-ae7d0425fa47"
            },
            {
                "name": "smartthings-multi-01",
                "uuid": "d5e8780a-1605-4992-b9a8-1f0744691b07"
            }
]

def searchByDeviceUuid(uuid):
    for device in devices:
        if device["uuid"] == uuid:
            return device

def searchByDeviceName(name):
    for device in devices:
        if device["name"] == name:
            return device