# How to Start the Project (Run Commands Only)

Assuming all initial setup and installations are complete, open **5 separate terminal windows** at the root folder of this project (`Generative Ai Fake News Detection and More`) and run the following commands.

### Terminal 1: Infrastructure (Redis & RabbitMQ)
```bash
cd backend
docker-compose up -d
```

### Terminal 2: API Gateway (Port 8000)
```bash
cd backend
.\venv\Scripts\python -m uvicorn gateway.main:app --port 8000 --host 127.0.0.1
```

### Terminal 3: Content Service (Port 8001)
```bash
cd backend
.\venv\Scripts\python -m uvicorn content_service.main:app --port 8001
```

### Terminal 4: Video Worker Service
```bash
cd backend\video_service
..\venv\Scripts\python main.py
```

### Terminal 5: Frontend UI (Port 5173)
```bash
cd frontend
npm run dev
```

---

**Access URLs:**
* **Frontend Application:** http://localhost:5173/
* **Gateway API Docs:** http://localhost:8000/docs
* **Content Service API Docs:** http://localhost:8001/docs
