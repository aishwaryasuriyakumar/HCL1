
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { GeneratePath } from './pages/GeneratePath';
import { PathResult } from './pages/PathResult';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/generate" element={<GeneratePath />} />
        <Route path="/path/:pathId" element={<PathResult />} />
      </Routes>
    </Router>
  );
}

export default App;
