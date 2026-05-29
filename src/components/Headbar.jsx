import { useTheme } from "../context/ThemeContext";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext"; 

const NAV_ITEMS = [
  { label: "Shop" },
  { label: "Collections" },
  { label: "About" },
  { label: "Contact" },
];

function Headbar({ searchQuery, setSearchQuery }) {
  const { darkMode, toggleTheme } = useTheme();
  const { itemCount } = useCart();
  const { user, setIsAuthOpen, logout } = useAuth(); 

  return (
    <header className="header">
      <div className="header-brand">
        <span className="brand-mark">MS</span>
        <div>
          <span className="brand-name">MiniShop</span>
          <span className="brand-tagline">
            Curated essentials, better shopping
          </span>
        </div>
      </div>

      <nav className="header-nav">
        {NAV_ITEMS.map((item) => (
          <span key={item.label} className="nav-link">
            {item.label}
          </span>
        ))}
      </nav>

      <div className="header-actions">
        <input
          type="text"
          placeholder="Search items..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            padding: '6px 12px',
            borderRadius: '6px',
            border: '1px solid var(--border)',
            background: 'var(--bg-input)',
            color: 'var(--text)',
            fontSize: '14px',
          }}
        />

        <button type="button" className="btn btn-sm btn-ghost" onClick={toggleTheme}>
          {darkMode ? '☀️ Light' : '🌙 Dark'}
        </button>

        <button type="button" className="btn btn-sm btn-ghost">
          🛒 Cart ({itemCount})
        </button>

        
        {user ? (
          <button type="button" className="btn btn-sm btn-ghost" onClick={logout} title="Click to logout">
            👤 {user.name}
          </button>
        ) : (
          <button type="button" className="btn btn-sm btn-primary" onClick={() => setIsAuthOpen(true)}>
            Sign In
          </button>
        )}
      </div>
    </header>
  );
}

export default Headbar;