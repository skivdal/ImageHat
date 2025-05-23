import * as duckdb from '@duckdb/duckdb-wasm';

import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    mvp: {
        mainModule: duckdb_wasm,
        mainWorker: mvp_worker,
    },
    eh: {
        mainModule: duckdb_wasm_eh,
        mainWorker: eh_worker,
    },
};

const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);

const worker = new Worker(bundle.mainWorker!);
const logger = new duckdb.VoidLogger();

const db = new duckdb.AsyncDuckDB(logger, worker);
await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

await db.registerFileURL("updated_dataset.csv", "/updated_dataset.csv", duckdb.DuckDBDataProtocol.HTTP, false);
await (await db.connect()).insertCSVFromPath("updated_dataset.csv", {
    schema: 'main',
    name: 'image_metadata',
    detect: true,
    header: true,
    delimiter: ',',
});


// Registering dataset for correct tag order
// Important for clean usage and standard conformity

await db.registerFileURL("exif_baseline_filtered.csv", "/exif_baseline_filtered.csv", duckdb.DuckDBDataProtocol.HTTP, false);
await (await db.connect()).insertCSVFromPath("exif_baseline_filtered.csv", {
    name: "exif_baseline",
    detect: true,
    header: true
});

//const conn = await db.connect();
//const tables = await conn.query("SHOW TABLES;");
//console.log("Tables loaded into DuckDB:", tables.toArray());



export { db };
