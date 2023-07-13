import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { About } from "./components/About";
import { Data } from "./components/Data";
function App() {
  return (
    <Router>
      <Navbar />

      <div>
        <Routes>
          <Route path="/about" element={<About />} />
          <Route path="/" element={<Data />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
