import { createFileRoute } from '@tanstack/react-router'
import * as React from 'react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export const Route = createFileRoute('/upload')({
  component: UploadComponent,
})

function UploadComponent() {
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null)
  const [jsonResponse, setJsonResponse] = React.useState<unknown>(null)
  const [error, setError] = React.useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0])
      setJsonResponse(null) // Reset previous results
      setError(null)
    }
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedFile) {
      toast.error('Please select a file first.')
      return
    }

    setIsSubmitting(true)
    setError(null)
    setJsonResponse(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Could not read error response.');
        throw new Error(
          `Upload failed with status: ${response.status}. ${errorText}`,
        )
      }

      const data = await response.json()
      setJsonResponse(data)
      toast.success('File uploaded and processed successfully!')
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'An unknown error occurred.'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="container mx-auto p-4 md:p-8">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>ImageHat Forensic EXIF Parser</CardTitle>
          <CardDescription>
            Upload a JPEG image to see its rich EXIF metadata
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="picture">Picture</Label>
                <Input
                  id="picture"
                  type="file"
                  onChange={handleFileChange}
                  accept="image/jpeg,image/png,image/tiff"
                  className="file:text-foreground"
                />
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button type="submit" disabled={!selectedFile || isSubmitting} className='mt-2'>
              {isSubmitting ? 'Uploading...' : 'Upload & Process'}
            </Button>
          </CardFooter>
        </form>
      </Card>

      {jsonResponse && (
        <Card className="max-w-2xl mx-auto mt-6">
          <CardHeader>
            <CardTitle>Response</CardTitle>
            <CardDescription>
              The following data was returned from the server
            </CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="p-4 bg-secondary rounded-md overflow-x-auto text-secondary-foreground text-sm">
              {JSON.stringify(jsonResponse, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}

      {error && (
        <Card className="max-w-2xl mx-auto mt-6 bg-destructive/10 border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-destructive font-mono">{error}</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}