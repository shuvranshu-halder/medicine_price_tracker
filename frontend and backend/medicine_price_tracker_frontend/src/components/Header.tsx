function Header(){
    return (
        <div>
            <nav className="navbar navbar-expand-lg bg-success">
                <div className="container-fluid">
                <a className="navbar-brand text-white fs-2" href="#">Medprice</a>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mb-2 mb-lg-0">
                    <li className="nav-item">
                        <a className="nav-link active text-white" aria-current="page" href="#"></a>
                    </li>
                    </ul>
                    <form className="d-flex ms-auto" role="search">
                    <button className="btn btn-outline-light" type="submit">see recent searches</button>
                    </form>
                </div>
                </div>
            </nav>
        </div>

    );
}

export default Header;