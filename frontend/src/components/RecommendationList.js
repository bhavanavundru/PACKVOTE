import React from "react";
import { MapPin } from "lucide-react";

const RecommendationList = ({ recommendations }) => {
  return (
    <div className="bg-lightbg p-4 rounded-2xl border border-gray-700">
      <h2 className="text-xl font-semibold text-primary mb-3">AI Recommendations 🌍</h2>
      {recommendations.length === 0 && <p>No recommendations yet</p>}
      <ul className="space-y-3">
        {recommendations.map((item) => (
          <li
            key={item.id}
            className="bg-darkbg p-3 rounded-xl flex justify-between items-center hover:border-primary border border-transparent"
          >
            <div>
              <p className="font-medium text-lg">{item.name}</p>
              <p className="text-gray-400 text-sm">{item.tags.join(", ")}</p>
            </div>
            <div className="text-right">
              <p className="text-primary font-semibold">{item.score.toFixed(2)}</p>
              <p className="text-gray-400 flex items-center gap-1 text-sm">
                <MapPin size={14} /> ₹{item.price}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecommendationList;
