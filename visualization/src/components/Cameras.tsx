import {useEffect, useState} from "react";
import BarChart, {DataPoint} from "../BarChart.tsx";

async function getTagNames() {
    const { db } = await import("../duckdb");
    const conn = await db.connect();

    //const r = await conn.query("SELECT DISTINCT tag_name FROM image_metadata ORDER BY tag_name;");
    //const tagNames = r.toArray().map(r => r.tag_name);
    const result = await conn.query(`
        SELECT "Tag Name" AS tag_name 
        FROM exif_baseline 
        ORDER BY CAST("Tag (Decimal)" AS INTEGER) ASC;
    `);
    const tagNames = result.toArray().map(r => r.tag_name);
    await conn.close()

    return tagNames;
}

async function getCameraNames(tagName: string) {
    const { db } = await import("../duckdb");
    const conn = await db.connect();
    const statement = await conn.prepare("\
        WITH cutter AS (\
            SELECT image_name, tag_name,\
                SUBSTR(image_name, 1, LENGTH(image_name) - POSITION('_' IN reverse(image_name))) as do_not_use\
            FROM image_metadata\
        )\
        SELECT\
            SUBSTR(d.image_name, 1, LENGTH(c.do_not_use) - POSITION('_' IN reverse(c.do_not_use))) AS camera_name,\
                tag_order,\
            COUNT(*) AS picture_count,\
        FROM image_metadata d\
        INNER JOIN cutter c ON d.image_name = c.image_name AND d.tag_name = c.tag_name\
        WHERE c.tag_name = ?\
        GROUP BY camera_name, tag_order\
        ORDER BY tag_order, camera_name;\
    ");

    const result = await statement.query(tagName);
    const groupedData: Record<number, { cameraName: string; pictureCount: number }[]> = result.toArray().reduce((acc, row) => {
        const tagOrder = Number(row.tag_order);
        const cameraName = row.camera_name;
        const pictureCount = Number(row.picture_count);

        if (!acc[tagOrder]) {
            acc[tagOrder] = [];
        }
        acc[tagOrder].push({ cameraName, pictureCount });
        return acc;
    }, {});

    return Object.entries(groupedData).map(([tagOrder, cameras]) => ({
        tagOrder: tagOrder,
        cameras,
    }));
}

const Cameras = () => {
    const [tagNames, setTagNames] = useState<string[]>([]);
    const [selectedTag, setSelectedTag] = useState<string>("");
    const [cameraCounts, setCameraCounts] = useState<DataPoint[]>([]);
    const [cameraNames, setCameraNames] = useState<{ tagOrder: string; cameras: { cameraName: string; pictureCount: number }[] }[]>([]);

    useEffect(() => {
        (async () => {
            const x = await getTagNames();
            setTagNames(x);
            setSelectedTag(x[0]);
        })();
    }, []);

    useEffect(() => {
        (async () => {
            if (!tagNames.includes(selectedTag)) {
                return;
            }
            const names = await getCameraNames(selectedTag);
            setCameraNames(names);
            const counts = names.map(location => ({
                tagOrder: location.tagOrder,
                count: location.cameras.length,
            }));
            setCameraCounts(counts);
        })();
    }, [selectedTag, tagNames]);

    return (
        <>
            <div className={"content"}>
                <div className={"content-child"}>
                    <label htmlFor="tagSelect">Select tag: </label>
                    <select id="tagSelect" name="tagSelect" onChange={e => setSelectedTag(e.target.value)} value={selectedTag}>
                        {tagNames.map(n => (
                            <option key={n}>{n}</option>
                        ))}
                    </select>
                    <br />
                    <BarChart data={cameraCounts} message={"Number of cameras"} />
                </div>
                <div className={"content-child"}>
                    {cameraNames.length > 0 && (
                        <ul>
                            {cameraNames.map((location, index) => (
                                <li key={index}>
                                    <strong>Loc {location.tagOrder}</strong>
                                    <ul>
                                        {location.cameras.map((camera, camIndex) => (
                                            <li key={camIndex}>
                                                {camera.cameraName}: {camera.pictureCount} imgs
                                            </li>
                                        ))}
                                    </ul>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </>
    );
};

export default Cameras;