import React, { useState } from "react";
import MedicineResults from "./medicineResults";

interface MedicineInfo {
  name: string;
  MRP: string | null;
  Discount: string | null;
  selling_price: string | null;
}

function Body() {
  const [medicine, setMedicine] = useState<string>("");

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

  const storeMedicine = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!medicine.trim()) return;

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
        {searched && !loading && !PEloading && !NMloading && !APloading &&  (
        <button
          onClick={downloadPDF}
          className="btn mt-3 px-4 py-2 text-white"
          style={{
            background: "linear-gradient(90deg, #1e7e34, #28a745)",
            borderRadius: "12px",
            border: "none",
            boxShadow: "0 4px 10px rgba(0,0,0,0.15)",
            fontWeight: 600,
            fontSize: "16px"
          }}
        >
          <i className="bi bi-download"></i>Download PDF
        </button>
      )}
      </div>
    </>
  );
}

export default Body;
