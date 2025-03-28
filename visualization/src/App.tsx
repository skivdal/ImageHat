import { useEffect } from 'react';
import db from './duckdb';
// @ts-ignore
import LinePlot from './LinePlot.jsx';

const App = () => {
  useEffect(() => {
    async function runQuery() {
      const conn = await db.connect();
      const result = await conn.query('SELECT 42 AS answer');
      console.log(result);
    }
    runQuery();
  }, []);

  return (
    <div>
      <h1>DuckDB-Wasm with React and Vite</h1>
      <LinePlot data={[1, 2, 3, 1, 2, 3, 22]} />
    </div>
  );
};

export default App;

