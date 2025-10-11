import React, { useState } from "react";
import ChatBox from "../components/ChatBox";
import RecommendationList from "../components/RecommendationList";
import RankingPanel from "../components/RankingPanel";
import axios from "axios";

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async (user, message) => {
    const updated = [...messages, { user_id: user, message }];
    setMessages(updated);
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/plan/", {
        messages: updated,
        top_k: 5,
      });
      setResults(res.data);
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-[90%] max-w-5xl mx-auto py-6">
      <h1 className="text-3xl font-bold text-primary mb-6 text-center">PACKVOTE 🧠</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <ChatBox onSend={handleSend} />
        {loading ? (
          <p className="text-center animate-pulse text-gray-400">AI Planning your trip...</p>
        ) : (
          results && (
            <div className="space-y-6">
              <RecommendationList recommendations={results.recommended_places} />
              <RankingPanel ranking={results.final_ranking} />
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default Home;
