import logo from '../assets/logo.png'; 

function Header() {
  return (
    <div>
      <nav className="navbar navbar-expand-lg bg-success">
        <div className="container-fluid">
          
          <a className="navbar-brand text-white d-flex align-items-center" href="#">
            <img 
              src={logo} 
              alt="Medprice Logo" 
              // *** FURTHER INCREASED HEIGHT TO 60px ***
              style={{ height: '80px', marginRight: '15px' }} 
            />
          </a>

          <div className="collapse navbar-collapse">
            <ul className="navbar-nav mb-2 mb-lg-0"></ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Header;