function Footer(){
    return (
        <>
        <footer className="bg-success text-white text-center py-3 mt-auto">
        <div className="container">
            <p className="mb-1 fs-5">Medprice</p>
            <p className="mb-0">Compare medicine prices across leading pharmacies</p>
            <hr className="border-light opacity-50 w-50 mx-auto my-2" />
            <p className="mb-0">© {new Date().getFullYear()} Medprice. All rights reserved.</p>
        </div>
    </footer>

        </>
    );
}

export default Footer;