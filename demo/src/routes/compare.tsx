import { createFileRoute } from "@tanstack/react-router";
import * as React from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  diff_match_patch,
  DIFF_DELETE,
  DIFF_INSERT,
  DIFF_EQUAL,
} from "diff-match-patch";

export const Route = createFileRoute("/compare")({
  component: CompareComponent,
});

const DiffView = ({ diff }: { diff: [number, string][] }) => {
  const lines = React.useMemo(() => {
    const dmp = new diff_match_patch();
    const outputLines: {
      type: "added" | "removed" | "equal";
      lineNumberLeft: number | null;
      lineNumberRight: number | null;
      content: React.ReactNode;
    }[] = [];

    let lineBuffer: [number, string][] = [];
    let leftLineNum = 1;
    let rightLineNum = 1;

    const processBuffer = () => {
      if (lineBuffer.length === 0) return;

      const hasDeletion = lineBuffer.some(([type]) => type === DIFF_DELETE);
      const hasInsertion = lineBuffer.some(([type]) => type === DIFF_INSERT);

      if (hasDeletion && hasInsertion) {
        // Modified line
        const leftText = lineBuffer
          .filter(([type]) => type !== DIFF_INSERT)
          .map(([, text]) => text)
          .join("");
        const rightText = lineBuffer
          .filter(([type]) => type !== DIFF_DELETE)
          .map(([, text]) => text)
          .join("");

        const charDiff = dmp.diff_main(leftText, rightText);
        dmp.diff_cleanupSemantic(charDiff);

        outputLines.push({
          type: "removed",
          lineNumberLeft: leftLineNum++,
          lineNumberRight: null,
          content: (
            <>
              {charDiff.map(([type, text], i) => {
                if (type === DIFF_INSERT) return null;
                const style =
                  type === DIFF_DELETE
                    ? { backgroundColor: "rgba(248, 81, 73, 0.4)" }
                    : {};
                return (
                  <span key={i} style={style}>
                    {text}
                  </span>
                );
              })}
            </>
          ),
        });

        outputLines.push({
          type: "added",
          lineNumberLeft: null,
          lineNumberRight: rightLineNum++,
          content: (
            <>
              {charDiff.map(([type, text], i) => {
                if (type === DIFF_DELETE) return null;
                const style =
                  type === DIFF_INSERT
                    ? { backgroundColor: "rgba(46, 160, 67, 0.4)" }
                    : {};
                return (
                  <span key={i} style={style}>
                    {text}
                  </span>
                );
              })}
            </>
          ),
        });
      } else if (hasDeletion) {
        // Deletion only
        const content = lineBuffer.map(([, text]) => text).join("");
        outputLines.push({
          type: "removed",
          lineNumberLeft: leftLineNum++,
          lineNumberRight: null,
          content: <>{content}</>,
        });
      } else if (hasInsertion) {
        // Insertion only
        const content = lineBuffer.map(([, text]) => text).join("");
        outputLines.push({
          type: "added",
          lineNumberLeft: null,
          lineNumberRight: rightLineNum++,
          content: <>{content}</>,
        });
      } else {
        // Equal line
        const content = lineBuffer.map(([, text]) => text).join("");
        outputLines.push({
          type: "equal",
          lineNumberLeft: leftLineNum++,
          lineNumberRight: rightLineNum++,
          content: <>{content}</>,
        });
      }

      lineBuffer = [];
    };

    diff.forEach(([type, text]) => {
      const textLines = text.split("\n");
      textLines.forEach((linePart, index) => {
        if (linePart) {
          lineBuffer.push([type, linePart]);
        }
        if (index < textLines.length - 1) {
          processBuffer();
        }
      });
    });
    processBuffer(); // Process any remaining buffer

    return outputLines;
  }, [diff]);

  return (
    <pre className="p-4 bg-secondary rounded-md overflow-x-auto text-secondary-foreground text-sm">
      <code>
        {lines.map((line, index) => {
          let bgColor = "";
          if (line.type === "added") bgColor = "bg-green-600/10";
          if (line.type === "removed") bgColor = "bg-red-600/10";

          return (
            <div key={index} className={`flex ${bgColor}`}>
              <span className="w-10 text-right pr-4 opacity-50 select-none">
                {line.lineNumberLeft}
              </span>
              <span className="w-10 text-right pr-4 opacity-50 select-none">
                {line.lineNumberRight}
              </span>
              <span className="w-4 text-center select-none">
                {line.type === "added"
                  ? "+"
                  : line.type === "removed"
                  ? "-"
                  : null}
              </span>
              <span className="flex-1 whitespace-pre-wrap">{line.content}</span>
            </div>
          );
        })}
      </code>
    </pre>
  );
};

const JsonView = ({ json }: { json: unknown }) => {
  const text = JSON.stringify(json, null, 2);
  const lines = text.split("\n");
  return (
    <pre className="p-4 bg-secondary rounded-md overflow-x-auto text-secondary-foreground text-sm">
      <code>
        {lines.map((line, index) => (
          <div key={index} className="flex">
            <span className="w-10 text-right pr-4 opacity-50 select-none">
              {index + 1}
            </span>
            <span className="flex-1 whitespace-pre-wrap">{line}</span>
          </div>
        ))}
      </code>
    </pre>
  );
};

function CompareComponent() {
  const [file1, setFile1] = React.useState<File | null>(null);
  const [file2, setFile2] = React.useState<File | null>(null);
  const [jsonResponse1, setJsonResponse1] = React.useState<unknown>(null);
  const [jsonResponse2, setJsonResponse2] = React.useState<unknown>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [diff, setDiff] = React.useState<[number, string][] | null>(null);

  React.useEffect(() => {
    if (jsonResponse1 && jsonResponse2) {
      const dmp = new diff_match_patch();
      const text1 = JSON.stringify(jsonResponse1, null, 2);
      const text2 = JSON.stringify(jsonResponse2, null, 2);
      const d = dmp.diff_main(text1, text2);
      dmp.diff_cleanupSemantic(d);
      setDiff(d);
    } else {
      setDiff(null);
    }
  }, [jsonResponse1, jsonResponse2]);

  const handleFile1Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile1(event.target.files[0]);
      setJsonResponse1(null);
      setError(null);
    }
  };

  const handleFile2Change = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile2(event.target.files[0]);
      setJsonResponse2(null);
      setError(null);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file1 || !file2) {
      toast.error("Please select both files first.");
      return;
    }

    setIsSubmitting(true);
    setError(null);
    setJsonResponse1(null);
    setJsonResponse2(null);

    const uploadFile = async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        const errorText = await response
          .text()
          .catch(() => "Could not read error response.");
        throw new Error(
          `Upload failed for ${file.name} with status: ${response.status}. ${errorText}`,
        );
      }
      return response.json();
    };

    try {
      const [data1, data2] = await Promise.all([
        uploadFile(file1),
        uploadFile(file2),
      ]);
      setJsonResponse1(data1);
      setJsonResponse2(data2);
      toast.success("Files uploaded and processed successfully!");
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "An unknown error occurred.";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto p-4 md:p-8">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>Compare Image Metadata</CardTitle>
          <CardDescription>
            Upload two JPEG images to compare their EXIF metadata
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="picture1">First Image</Label>
                <Input
                  id="picture1"
                  type="file"
                  onChange={handleFile1Change}
                  accept="image/jpeg,image/png,image/tiff"
                  className="file:text-foreground"
                />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="picture2">Second Image</Label>
                <Input
                  id="picture2"
                  type="file"
                  onChange={handleFile2Change}
                  accept="image/jpeg,image/png,image/tiff"
                  className="file:text-foreground"
                />
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button
              type="submit"
              disabled={!file1 || !file2 || isSubmitting}
              className="mt-2"
            >
              {isSubmitting ? "Comparing..." : "Compare Metadata"}
            </Button>
          </CardFooter>
        </form>
      </Card>

      {jsonResponse1 && jsonResponse2 && (
        <div className="max-w-7xl mx-auto mt-6">
          {diff && (
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Metadata Difference</CardTitle>
                <CardDescription>
                  Showing differences between the two metadata files. Green for
                  additions, red for removals.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <DiffView diff={diff} />
              </CardContent>
            </Card>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>First Image Metadata</CardTitle>
              </CardHeader>
              <CardContent>
                <JsonView json={jsonResponse1} />
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Second Image Metadata</CardTitle>
              </CardHeader>
              <CardContent>
                <JsonView json={jsonResponse2} />
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {error && (
        <Card className="max-w-4xl mx-auto mt-6 bg-destructive/10 border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-destructive font-mono">{error}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
