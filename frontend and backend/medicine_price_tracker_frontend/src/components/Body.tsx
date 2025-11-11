import React, { useState } from "react";
import MedicineResults from "./medicineResults";

interface MedicineInfo {
  name: string;
  MRP: string | null;
  Discount: string | null;
  selling_price: string | null;
}

function Body() {
  // getting medicine name from user input
  const [medicine, setMedicine] = useState<string>("");

  //tata1mg
  const [tata1mgResult, setTata1mgResult] = useState<MedicineInfo[] | null>(
    null
  );
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState<boolean>(false); 
  //pharmeasy
  const [PEResult, setPEResult] = useState<MedicineInfo[] | null>(
    null
  );
  const [PEloading, setPELoading] = useState<boolean>(false);
  const [PEerror, setPEError] = useState<string | null>(null);
  const [PEsearched, setPESearched] = useState<boolean>(false); 

  //netmeds
  const [NMResult, setNMResult] = useState<MedicineInfo[] | null>(
    null
  );
  const [NMloading, setNMLoading] = useState<boolean>(false);
  const [NMerror, setNMError] = useState<string | null>(null);
  const [NMsearched, setNMSearched] = useState<boolean>(false); 
  //apollo
    const [APResult, setAPResult] = useState<MedicineInfo[] | null>(
    null
  );
  const [APloading, setAPLoading] = useState<boolean>(false);
  const [APerror, setAPError] = useState<string | null>(null);
  const [APsearched, setAPSearched] = useState<boolean>(false); 

  const storeMedicine = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!medicine.trim()) return;
    //tata1mg
    setSearched(true); 
    setLoading(true);
    setError(null);
    setTata1mgResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/tata1mg?medicine_name=${encodeURIComponent(
          medicine
        )}`
      );

      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setTata1mgResult(result);
    } catch (err) {
      console.error(err);
      setError("❌ server down.");
    } finally {
      setLoading(false);
    }


    //pharmeasy
    setPESearched(true); 
    setPELoading(true);
    setPEError(null);
    setPEResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/pharmeasy?medicine_name=${encodeURIComponent(
          medicine
        )}`
      );

      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setPEResult(result);
    } catch (err) {
      console.error(err);
      setPEError("❌ server down");
    } finally {
      setPELoading(false);
    }

    //netmeds
    setNMSearched(true); 
    setNMLoading(true);
    setNMError(null);
    setNMResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/netmeds?medicine_name=${encodeURIComponent(
          medicine
        )}`
      );

      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setNMResult(result);
    } catch (err) {
      console.error(err);
      setNMError("❌ server down.");
    } finally {
      setNMLoading(false);
    }
    //apollo
    setAPSearched(true); 
    setAPLoading(true);
    setAPError(null);
    setAPResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/apollo?medicine_name=${encodeURIComponent(
          medicine
        )}`
      );

      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setAPResult(result);
    } catch (err) {
      console.error(err);
      setAPError("❌ server down");
    } finally {
      setAPLoading(false);
    }
  };

  return (
    <>
      <div
        className="d-flex flex-column justify-content-center align-items-center min-vh-100"
        style={{
          backgroundImage: "url('./src/assets/bg_image.png')",
          backgroundSize: "cover",
          backgroundRepeat: "repeat",
          backgroundPosition: "center",
          backgroundBlendMode: "lighten",
          backgroundColor: "#e4e8e5ff",
          paddingBottom: "120px",
          paddingTop: "40px",

        }}
      >
        <form
          className="d-flex w-75 w-md-50 shadow-lg p-3 bg-white rounded"
          role="search"
          onSubmit={storeMedicine}
        >
          <input
            className="form-control form-control-lg me-2"
            type="search"
            placeholder="Search for medicine prices..."
            aria-label="Search"
            value={medicine}
            onChange={(e) => setMedicine(e.target.value)}
          />
          <button className="btn btn-success btn-lg" type="submit">
            Search
          </button>
        </form>

          <MedicineResults
            siteName="Tata 1mg"
            searched={searched}
            loading={loading}
            error={error}
            results={tata1mgResult}
          />

          <MedicineResults
            siteName="Pharmeasy"
            searched={PEsearched}
            loading={PEloading}
            error={PEerror}
            results={PEResult}
          />

          <MedicineResults
            siteName="Netmeds"
            searched={NMsearched}
            loading={NMloading}
            error={NMerror}
            results={NMResult}
          />

          <MedicineResults
            siteName="Apollo"
            searched={APsearched}
            loading={APloading}
            error={APerror}
            results={APResult}
          />

      </div>
    </>
  );
}


export default Body;
