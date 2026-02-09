---
layout: default
title: Backend Architecture
parent: Architecture
---

# Backend Architecture

## 1. 개요 (Overview)
이 문서는 Django 기반의 QuizRPG 프로젝트의 백엔드 구조와 구성 요소를 설명합니다. 이 프로젝트는 RESTful API를 제공하며, 사용자 인증 및 권한 부여, 프로필 관리, 질문 및 게임 기능을 포함하고 있습니다. 

## 2. 아키텍처 및 로직 (Architecture & Logic)
QuizRPG 프로젝트는 Django 프레임워크를 기반으로 하며, 여러 앱으로 구성되어 있습니다. 주요 앱으로는 `accounts`, `questions`, `game`, `profiles`, `ai`가 있으며, 각각 사용자 관리, 질문 관리, 게임 로직, 프로필 관리, AI 기능을 담당합니다. Django의 기본 인증 시스템을 확장하여 사용자 인증 및 권한 부여를 처리하고, RESTful API를 통해 클라이언트와 상호작용합니다.

## 3. 핵심 컴포넌트 분석 (Key Components)

### 3.1 URL 라우팅
프로젝트의 URL 라우팅은 `QuizRPG/urls.py` 파일에서 정의되어 있으며, 각 앱의 URL을 포함합니다.

| 경로 (Route Path)           | HTTP 메서드 | 핸들러 함수 (Handler Function) | 목적 (Purpose)                     |
|:----------------------------|:-----------|:-------------------------------|:----------------------------------|
| `admin/`                    | GET        | `admin.site.urls`              | 관리자 페이지 접근                |
| `accounts/`                 | ALL        | `dj_rest_auth.urls`            | 사용자 인증 및 권한 부여          |
| `accounts/signup/`          | POST       | `dj_rest_auth.registration.urls` | 사용자 회원가입                   |
| `api/v1/questions/`         | ALL        | `questions.urls`               | 질문 관리 API                     |
| `api/v1/game/`              | ALL        | `game.urls`                    | 게임 관련 API                     |
| `api/v1/profile/`           | ALL        | `profiles.urls`                | 프로필 관리 API                   |
| `api/v1/ai/`                | ALL        | `ai.urls`                      | AI 관련 API                       |

### 3.2 사용자 모델
`accounts/models.py` 파일에서 사용자 모델은 Django의 기본 `AbstractUser`를 확장하여 정의되어 있습니다.

| 필드 이름 (Field Name) | 타입 (Type) | 제약 조건 (Constraints) | 설명 (Description)            |
|:-----------------------|:-----------|:-----------------------|:-----------------------------|
| 기본 제공 필드         | -          | -                      | Django의 기본 사용자 필드 사용 |

### 3.3 사용자 등록 API
`accounts/views.py` 파일에서 사용자 등록 API의 로직은 다음과 같습니다.

| 엔드포인트 (Endpoint) | 입력 파라미터 (Input Params) | 응답 모델 (Response Model) | 로직 요약 (Logic Summary) |
|:----------------------|:----------------------------|:--------------------------|:--------------------------|
| `register`            | `username`, `password`, `email` | `token`, `user`, `earned_badge` | 사용자 등록, 토큰 발급, 프로필 생성, 뱃지 지급 |

## 4. 사용 예시 (Usage)
다음은 사용자 등록 API의 사용 예시입니다.

```python
POST /register
{
    "username": "testuser",
    "password": "securepassword",
    "email": "user@example.com"
}
```

응답 예시:

```json
{
    "token": "abcd1234",
    "user": {
        "id": 1,
        "email": "user@example.com"
    },
    "earned_badge": {
        "id": 1,
        "code": "welcome",
        "name": "Welcome Badge",
        "description": "Welcome to the platform!",
        "icon": "welcome_icon.png"
    }
}
```

## 5. 설정 (Configuration)

### 환경 변수
프로젝트는 `.env` 파일을 통해 환경 변수를 관리합니다.

| 변수명 (Variable Name) | 설명 (Description)                      |
|:-----------------------|:---------------------------------------|
| `OPENAI_API_KEY`       | OpenAI API 키                          |
| `OPENAI_MODEL`         | 사용 모델 (기본값: `gpt-5-mini`)       |
| `GMS_KEY`              | GMS 서비스 키                          |

이 문서는 Django 기반의 QuizRPG 프로젝트의 백엔드 구조와 주요 컴포넌트에 대한 상세한 분석을 제공합니다. 각 구성 요소는 Django의 기능을 확장하여 구현되어 있으며, RESTful API를 통해 클라이언트와 상호작용합니다.