import './App.css';
import { BrowserRouter,Routes,Route,Link } from "react-router-dom";
import NavBar from './components/scripts/Navbar';
import Login from './components/scripts/Login';
import Dashboard from './components/scripts/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element = {<Login />} />
        <Route path="/home" element = {[<NavBar />, <Dashboard />] } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
