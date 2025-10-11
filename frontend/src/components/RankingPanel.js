import React from "react";
import { Star } from "lucide-react";

const RankingPanel = ({ ranking }) => {
  return (
    <div className="bg-lightbg p-4 rounded-2xl border border-gray-700">
      <h2 className="text-xl font-semibold text-primary mb-3">Final AI Ranking 🏆</h2>
      <ol className="space-y-3">
        {ranking.map((r, index) => (
          <li
            key={r.id}
            className="bg-darkbg p-3 rounded-xl flex justify-between items-center"
          >
            <span className="font-medium">
              #{index + 1} {r.name}
            </span>
            <span className="flex items-center text-primary font-semibold">
              <Star size={16} className="mr-1" />
              {r.score.toFixed(2)}
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
};

export default RankingPanel;
