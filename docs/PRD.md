# Project Requirements Document (PRD) – Vibe Coder Flashcards

## 1. Overview
Build a web app that tracks new AI tools, updates, techniques, protocols, and systems from select Twitter and YouTube feeds. It generates flashcards from these updates using an LLM and gamifies learning with daily memorization sprints and weekly quizzes.

## 2. Target Audience
- AI-curious developers ("vibe coders")
- Beginner to intermediate engineers exploring new tooling
- Hackathon competitors and indie AI tool builders

## 3. Core Features
1. Feed Listener: Follow selected X (Twitter) accounts and YouTube channels
2. Content Filter & LLM Summarizer: Summarize new content into concise, high-signal flashcards
3. Daily Deck: Deliver 15–30 flashcards per day to the user
4. Study Mode: Gamified study with timers, streak tracking, spaced repetition (SM-2)
5. Weekly Quiz: Randomized multiple-choice quiz on past week’s cards
6. Leaderboard & XP: Rank users by quiz scores; award XP, levels, and badges
7. Notifications: Daily deck drop, reminders to study, weekly quiz start

## 4. User Stories
- As a user, I want to follow selected accounts for AI updates
- As a user, I want flashcards created automatically from daily posts
- As a user, I want to study daily and track my streaks
- As a user, I want to compete on a weekly quiz and see my rank

## 5. Functional Requirements
- Feed ingestion (Twitter, YouTube)
- Summarization via LLM
- Flashcard generation, scheduling, and scoring
- User authentication, storage, and profile tracking
- Real-time leaderboard and streak engine

## 6. Non-functional Requirements
- Mobile-friendly, responsive design
- Modular backend architecture (worker queues, microservices)
- Caching and rate limiting for API use
- Secure storage and authentication (OAuth 2.0 or magic link)

## 7. KPIs
- % of cards studied per user per day
- Quiz participation rate
- Avg. flashcards retained (recalled correctly 2+ times)
- Leaderboard engagement rate
