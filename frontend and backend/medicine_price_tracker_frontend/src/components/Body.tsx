import React, { useState } from "react";
import MedicineResults from "./medicineResults";
import { useEffect } from "react";

interface MedicineInfo {
  name: string;
  MRP: string | null;
  Discount: string | null;
  selling_price: string | null;
}

function Body() {
  
  const [medicine, setMedicine] = useState<string>("");
  const [searchCount, setSearchCount] = useState<number>(0);
  const [animatedCount, setAnimatedCount] = useState<number>(0);


  // state variables
  const [tata1mgResult, setTata1mgResult] = useState<MedicineInfo[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState<boolean>(false);

  const [PEResult, setPEResult] = useState<MedicineInfo[] | null>(null);
  const [PEloading, setPELoading] = useState<boolean>(false);
  const [PEerror, setPEError] = useState<string | null>(null);
  const [PEsearched, setPESearched] = useState<boolean>(false);

  const [NMResult, setNMResult] = useState<MedicineInfo[] | null>(null);
  const [NMloading, setNMLoading] = useState<boolean>(false);
  const [NMerror, setNMError] = useState<string | null>(null);
  const [NMsearched, setNMSearched] = useState<boolean>(false);

  const [APResult, setAPResult] = useState<MedicineInfo[] | null>(null);
  const [APloading, setAPLoading] = useState<boolean>(false);
  const [APerror, setAPError] = useState<string | null>(null);
  const [APsearched, setAPSearched] = useState<boolean>(false);

  // ---------------- PDF DOWNLOAD FUNCTION ----------------
  const downloadPDF = async () => {
    const results = {
      Tata1mg: tata1mgResult,
      Pharmeasy: PEResult,
      Netmeds: NMResult,
      Apollo: APResult,
    };

    const response = await fetch("http://127.0.0.1:5000/download-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ medicine, results }),
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${medicine}_prices.pdf`;
    a.click();
  };
  // ---------------------------------------------------------
  useEffect(() => {
    if (searchCount === 0) {
      setAnimatedCount(0);
      return;
    }

    let start = 0;
    const end = searchCount;
    const duration = 800; // animation speed in ms
    const stepTime = 10;
    const increment = end / (duration / stepTime);

    const timer = setInterval(() => {
      start += increment;

      if (start >= end) {
        start = end;
        clearInterval(timer);
      }

      setAnimatedCount(Math.floor(start));
    }, stepTime);

    return () => clearInterval(timer);
  }, [searchCount]);

  const storeMedicine = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!medicine.trim()) return;

    //update database
    await fetch("http://127.0.0.1:5000/start-search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ medicine }),
    });

    //count of the searched medicine
    const countRes = await fetch(
      `http://127.0.0.1:5000/get-count?medicine=${encodeURIComponent(medicine)}`
    );
    const countData = await countRes.json();
    setSearchCount(countData.count);


    // tata1mg
    setSearched(true);
    setLoading(true);
    setError(null);
    setTata1mgResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/tata1mg?medicine_name=${encodeURIComponent(medicine)}`
      );
      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setTata1mgResult(result);
    } catch (err) {
      console.error(err)
      setError("❌ server down.");
    } finally {
      setLoading(false);
    }

    // pharmeasy
    setPESearched(true);
    setPELoading(true);
    setPEError(null);
    setPEResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/pharmeasy?medicine_name=${encodeURIComponent(medicine)}`
      );
      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setPEResult(result);
    } catch (err) {
      console.error(err)
      setPEError("❌ server down");
    } finally {
      setPELoading(false);
    }

    // netmeds
    setNMSearched(true);
    setNMLoading(true);
    setNMError(null);
    setNMResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/netmeds?medicine_name=${encodeURIComponent(medicine)}`
      );
      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setNMResult(result);
    } catch (err) {
      console.error(err)
      setNMError("❌ server down.");
    } finally {
      setNMLoading(false);
    }

    // apollo
    setAPSearched(true);
    setAPLoading(true);
    setAPError(null);
    setAPResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/apollo?medicine_name=${encodeURIComponent(medicine)}`
      );
      if (!response.ok) throw new Error("Server Error");

      const result: MedicineInfo[] = await response.json();
      setAPResult(result);
    } catch (err) {
      console.error(err)
      setAPError("❌ server down");
    } finally {
      setAPLoading(false);
    }
  };

  return (
    <>
      {/* pdf download button */}
      {searched && !loading && !PEloading && !NMloading && !APloading && (
        <div className="d-flex justify-content-end mt-3 w-100">
        <button
          onClick={downloadPDF}
          className="btn px-4 py-2 text-white me-5" 
          style={{
            background: "linear-gradient(90deg, #1e7e34, #28a745)",
            borderRadius: "12px",
            border: "none",
            boxShadow: "0 4px 10px rgba(0,0,0,0.15)",
            fontWeight: 600,
            fontSize: "16px"
          }}
        >
          <i className="bi bi-download"></i> Download PDF
        </button>
      </div>
      )}


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
          onSubmit={storeMedicine}
        >
          <input
            className="form-control form-control-lg me-2"
            type="search"
            placeholder="Search for medicine prices..."
            value={medicine}
            onChange={(e) => setMedicine(e.target.value)}
          />
          <button className="btn btn-success btn-lg" type="submit">
            Search
          </button>
        </form>

        {/* -------- DOWNLOAD BUTTON ---------- */}
        

        {/* ---------------------------------- */}

        <MedicineResults siteName="Tata 1mg" searched={searched} loading={loading} error={error} results={tata1mgResult} />
        <MedicineResults siteName="Pharmeasy" searched={PEsearched} loading={PEloading} error={PEerror} results={PEResult} />
        <MedicineResults siteName="Netmeds" searched={NMsearched} loading={NMloading} error={NMerror} results={NMResult} />
        <MedicineResults siteName="Apollo" searched={APsearched} loading={APloading} error={APerror} results={APResult} />
        
      {/* data visualization */}
      {searched && !loading && !PEloading && !NMloading && !APloading &&
       <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <div
          style={{
            backgroundColor: "white",
            border: "2px solid #198754",
            color: "#198754",
            borderRadius: "12px",
            padding: "10px 20px",
            fontWeight: 600,
            fontSize: "18px",
            boxShadow: "0 3px 8px rgba(0,0,0,0.1)",
            display: "inline-flex",
            width: "fit-content",
          }}
        >
         "{medicine}" searched {animatedCount} times
          {animatedCount !== 1 ? "s" : ""} till now
        </div>
      </div>}

      </div>
    </>
  );
}

export default Body;
