api:
	uvicorn main:app --reload

ngrok:
	ngrok http --domain=fit-katydid-related.ngrok-free.app 8000