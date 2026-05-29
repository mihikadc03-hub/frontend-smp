import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import { CartProvider } from "./context/CartContext";
import { ThemeProvider } from "./context/ThemeContext";
import { AuthProvider } from "./context/AuthContext"; 

import Headbar from "./components/Headbar";
import SigninPopup from "./components/SigninPopup"; 
import Home from "./pages/Home";
import ItemPage from "./pages/ItemPage";
import About from "./pages/About";
import Collections from "./pages/Collections";
import Contact from "./pages/Contact";

function App() {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <AuthProvider>
      <ThemeProvider>
        <CartProvider>
          <div className="app">
            <Headbar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
            <SigninPopup /> 

            <main className="app-content">
              <Routes>
                <Route path="/" element={<Home searchQuery={searchQuery} />} />
                <Route path="/collections" element={<Collections />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/item/:id" element={<ItemPage />} />
                <Route path="/about" element={<About />} />
              </Routes>
            </main>
          </div>
        </CartProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;