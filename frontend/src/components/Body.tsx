function Body(){
    return (
        <>
            <div
            className="d-flex justify-content-center align-items-center vh-100"
            style={{
                backgroundImage: "url('./src/assets/bg_image.png')",
                backgroundSize: 'cover',          // makes it fill nicely
                backgroundRepeat: 'repeat',       // repeats symmetrically
                backgroundPosition: 'center',
                backgroundBlendMode: 'lighten',
                backgroundColor: '#e4e8e5ff'      // fallback light background
            }}
            >
            <form className="d-flex w-75 w-md-50 shadow-lg p-3 bg-white rounded" role="search">
                <input
                className="form-control form-control-lg me-2"
                type="search"
                placeholder="search for medicine prices, or pharmacies..."
                aria-label="Search"
                />
                <button className="btn btn-success btn-lg" type="submit">
                Search
                </button>
            </form>
            </div>


        </>
    );
}

export default Body;