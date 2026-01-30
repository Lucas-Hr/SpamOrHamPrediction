"use client";
import { useState } from "react";
const Table = () => {
  // Initializing state with some dummy data
  const [data] = useState([
    { id: 1, message: "System heart rate stable", classification: "Spam", accuracy: "98.5%" },
    { id: 2, message: "Unexpected spike in CPU", classification: "Ham", accuracy: "92.1%" },
    { id: 3, message: "User login successful", classification: "Spam", accuracy: "100%" },
    { id: 4, message: "Database latency detected", classification: "Spam", accuracy: "85.4%" },
    { id: 5, message: "Backup completed", classification: "Spam", accuracy: "99.9%" },
    { id: 6, message: "API timeout on endpoint /v1/auth", classification: "Error", accuracy: "78.2%" },
    { id: 7, message: "Memory usage optimized", classification: "Spam", accuracy: "95.0%" },
    { id: 8, message: "New device connected", classification: "Ham", accuracy: "88.7%" },
    { id: 9, message: "Disk space low", classification: "Spam", accuracy: "91.2%" },
    { id: 10, message: "Cache invalidated", classification: "Spam", accuracy: "100%" },
  ]);

  return (
    <div className="w-full px-4">
      {/* Container that controls the height and scrolling */}
      <div className="relative overflow-y-auto border border-gray-200 rounded-lg shadow-sm h-75" >
        <table className="w-full text-sm text-left text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-100 sticky top-0 z-10">
            <tr>
              <th className="px-6 py-3">N°</th>
              <th className="px-6 py-3">Message</th>
              <th className="px-6 py-3">Classification</th>
              <th className="px-6 py-3">Précision</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {data.map((row) => (
              <tr key={row.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-medium text-gray-900">{row.id}</td>
                <td className="px-6 py-4">{row.message}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold 
                    ${row.classification === 'Spam' ? 'bg-red-100 text-red-700' : 
                
                      'bg-green-100 text-green-700'}`}>
                    {row.classification}
                  </span>
                </td>
                <td className="px-6 py-4">{row.accuracy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Table;