# DevSentry AI

An elite Static Application Security Testing (SAST) engine and AI Code Bug Detector.

## Project Overview
DevSentry AI helps developers find and fix Syntax Errors, Logical Flaws, Security Vulnerabilities, Resource Leaks, and Performance Bottlenecks automatically using an intelligent AI engine.

## Technology Stack
- **Frontend**: Single Page HTML Application, Vanilla JavaScript, Tailwind CSS (via CDN), Monaco Editor.
- **Backend**: Java 17, Spring Boot 3.3.4, Spring Security (JWT), Spring Data JPA.
- **Database**: H2 (In-memory development default) / MySQL (Production).
- **AI Integration**: Spring AI (OpenAI API).

## Folder Structure
```text
/
├── index.html                           (Main Frontend UI & Logic)
├── pom.xml                              (Maven Dependencies)
├── src/main/java/com/cs/bugdetector/
│   ├── controller/                      (REST Controllers)
│   ├── dto/                             (Data Transfer Objects)
│   ├── entity/                          (JPA Database Entities)
│   ├── repository/                      (Spring Data Repositories)
│   ├── security/                        (JWT & Spring Security Config)
│   ├── service/                         (AI & Mock Services)
│   └── DevSentryApplication.java        (Spring Boot Main Class)
└── src/main/resources/
    └── application.properties           (Config Variables)
```

## Prerequisites
- **Java**: JDK 17 (Required for Spring Boot 3)
- **Database**: None needed out-of-the-box (uses H2). To switch to MySQL, edit `application.properties`.

## How to Start the Application

### 1. Start the Backend
1. Open a terminal in the root directory.
2. Run `./mvnw spring-boot:run` (or use your IDE).
3. The server will start on `http://localhost:8080`.

*(Note: If `AI_API_KEY` is not provided, the backend will safely fallback to a Mock AI Provider so you can still demonstrate functionality.)*

### 2. Start the Frontend
1. Open `index.html` in your browser (e.g., via VS Code Live Server).
2. The UI will automatically communicate with the backend.

## API Documentation

**AUTH ENDPOINTS**
- `POST /api/auth/register` (Requires JSON: `username`, `email`, `password`)
- `POST /api/auth/login` (Requires JSON: `username`, `password`)
- `GET /api/auth/me` (Requires Header: `Authorization: Bearer <token>`)

**AUDIT ENDPOINTS**
- `POST /api/v1/detector/analyze` (Requires Header: `Authorization: Bearer <token>`, JSON: `language`, `sourceCode`)
- `GET /api/audits` (Requires Header: `Authorization: Bearer <token>`)
- `GET /api/audits/stats` (Requires Header: `Authorization: Bearer <token>`)

## Environment Variables (.env.example)
```properties
DATABASE_URL=jdbc:mysql://localhost:3306/devsentry
DATABASE_USERNAME=root
DATABASE_PASSWORD=secret
JWT_SECRET=8f7b243b8d4e9c71a35f6e8b4d2a1c9f0b7e5d3c1a9f6e4b2d8c0a5f3e7b1d9
AI_API_KEY=sk-your-openai-key
```
