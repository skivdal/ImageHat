import { useEffect, useState } from "react";
import BarChart from "../BarChart";

async function getTagNames() {
    // @ts-ignore
    const { db } = await import("../duckdb");

    const conn = await db.connect();
    const r = await conn.query("SELECT DISTINCT tag_name FROM image_metadata ORDER BY tag_name;");
    const tagNames = r.toArray().map(r => r.tag_name);

    return tagNames;
}

async function getOrderCounts(tagName: string) {
    const { db } = await import("../duckdb");

    const conn = await db.connect();
    const statement = await conn.prepare("\
    SELECT tag_order, count(image_name) as ct FROM image_metadata\
    WHERE tag_name = ? GROUP BY tag_order ORDER BY tag_order;\
  ");

    const result = await statement.query(tagName);
    return result.toArray().map(r => {
        const x = r.toJSON();
        return {
            tagOrder: Number(x.tag_order),
            count: Number(x.ct),
        };
    });
}

const Images = () => {
    const [tagNames, setTagNames] = useState<any[]>([]);
    const [selectedTag, setSelectedTag] = useState<string>("");
    const [orderCounts, setOrderCounts] = useState<any[]>([]);

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

            let x = await getOrderCounts(selectedTag);
            setOrderCounts(x);
        })();
    }, [selectedTag]);

    return (
        <div className="content">
            <div className={"content-child"}>
                <label htmlFor="tagSelect">Select tag: </label>
                <select id="tagSelect" name="tagSelect" onChange={e => setSelectedTag(e.target.value)}
                        value={selectedTag}>
                    {
                        tagNames.map(n => {
                            return <option key={n}>{n}</option>;
                        })
                    }
                </select>
                <br/>
               <BarChart data={orderCounts} message={"Number of images"}></BarChart>
            </div>
            <div className={"content-child"}>
                <ul>
                    {
                        orderCounts.map(x => {
                            return <li key={x.tagOrder}>
                                <p><strong>Loc {x.tagOrder}: </strong> {x.count} imgs</p>
                            </li>
                        })
                    }
                </ul>
            </div>
        </div>
    );
};

export default Images;