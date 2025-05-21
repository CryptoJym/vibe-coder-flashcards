import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [input, setInput] = useState('');
  const [summary, setSummary] = useState('');
  const [cards, setCards] = useState<{ question: string; answer: string }[]>([]);

  const handleSummarise = async () => {
    const { data } = await axios.post('/api/summarise', { text: input });
    setSummary(data.summary);
  };

  const handleFlashcards = async () => {
    const { data } = await axios.post('/api/flashcards', { text: input });
    setCards(data.flashcards);
  };

  return (
    <main className="max-w-2xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold text-center">Vibe Coder Flashcards</h1>
      <textarea
        className="w-full border rounded p-2"
        rows={4}
        placeholder="Paste text to summarise or convert to flashcards"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <div className="flex gap-2">
        <button
          onClick={handleSummarise}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Summarise
        </button>
        <button
          onClick={handleFlashcards}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Flashcards
        </button>
      </div>

      {summary && (
        <section>
          <h2 className="font-semibold">Summary</h2>
          <p>{summary}</p>
        </section>
      )}

      {cards.length > 0 && (
        <section>
          <h2 className="font-semibold">Flashcards</h2>
          <ul className="space-y-2">
            {cards.map((c, i) => (
              <li key={i} className="border rounded p-2">
                <p className="font-medium">Q: {c.question}</p>
                <p>A: {c.answer}</p>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
