import React from "react";

interface MedicineInfo {
  name: string;
  MRP?: string | null;
  Discount?: string | null;
  price_after_discount?: string | null;
  selling_price?: string | null;
}

interface MedicineResultsProps {
  siteName: string;
  searched: boolean;
  loading: boolean;
  error: string | null;
  results: MedicineInfo[] | null;
}

const MedicineResults: React.FC<MedicineResultsProps> = ({
  siteName,
  searched,
  loading,
  error,
  results,
}) => {
  if (!searched) return null;

  return (
    <div
  className="mt-4 mb-5 w-75 bg-white rounded shadow p-4"
  style={{
    // remove fixed maxHeight for small results
    overflow: results && results.length > 5 ? "hidden" : "visible",
    marginBottom: "40px", // ✅ space before footer
  }}
>
  {loading && (
    <div className="text-center text-secondary fs-5">
      <div className="spinner-border text-success me-2" role="status"></div>
      Searching {siteName} website...
    </div>
  )}

  {error && !loading && (
    <>
      <h3 className="text-center text-success mb-3">{siteName}</h3>
      <p className="text-danger text-center">{error}</p>
    </>
  )}

  {results && results.length > 0 && !loading && (
    <>
      <h3 className="text-center text-success mb-3">{siteName}</h3>

      {/* ✅ Scroll only if many results */}
      <div
        style={{
          maxHeight: results.length > 5 ? "45vh" : "none",
          overflowY: results.length > 5 ? "auto" : "visible",
          paddingBottom: "25px", // ✅ makes last row visible
        }}
      >
        <table className="table table-bordered table-striped mb-0">
          <thead
            className="table-success"
            style={{
              position: results.length > 5 ? "sticky" : "static",
              top: 0,
              backgroundColor: "#d1e7dd",
              zIndex: 1,
            }}
          >
            <tr>
              <th>Name</th>
              <th>MRP (₹)</th>
              <th>Discount (%)</th>
              <th>Price After Discount (₹)</th>
            </tr>
          </thead>
          <tbody>
            {results.map((item, index) => (
              <tr key={index}>
                <td>{item.name}</td>
                <td>{item.MRP ?? item.price_after_discount ?? "-"}</td>
                <td>{item.Discount ?? "-"}</td>
                <td>
                  {item.price_after_discount ?? item.selling_price ?? "-"}
                </td>
              </tr>
            ))}
            {/* ✅ spacer row for smooth scroll stop */}
            {results.length > 5 && (
              <tr>
                <td colSpan={4} style={{ height: "30px", border: "none" }}></td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  )}

  {results === null && !loading && !error && (
    <>
      <h3 className="text-center text-success mb-3">{siteName}</h3>
      <p className="text-center text-muted">No results found.</p>
    </>
  )}
</div>


  );
};

export default MedicineResults;
