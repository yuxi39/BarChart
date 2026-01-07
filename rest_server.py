from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import tempfile
import shutil
import zipfile
from pathlib import Path
import uvicorn
from recreate_sorted_chart import generate_chart

app = FastAPI(title='Chart Generator API')

class ChartConfig(BaseModel):
    title: str | None = None
    tag: str | None = None
    unit: str | None = None
    left_summary: str | None = None
    data: list | dict | None = None

@app.post('/generate')
async def generate(config: ChartConfig, fmt: str = Query('png', regex='^(png|svg|pptx|all)$')):
    """Generate chart and return requested file(s).

    fmt: png | svg | pptx | all
    """
    tmpdir = Path(tempfile.mkdtemp(prefix='chart-api-'))
    try:
        res = generate_chart(config.dict(), output_dir=tmpdir, overwrite_pptx=True)
    except Exception as e:
        shutil.rmtree(tmpdir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

    if fmt == 'png':
        return FileResponse(res['png'], media_type='image/png', filename=Path(res['png']).name)
    if fmt == 'svg':
        return FileResponse(res['svg'], media_type='image/svg+xml', filename=Path(res['svg']).name)
    if fmt == 'pptx':
        return FileResponse(res['pptx'], media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', filename=Path(res['pptx']).name)
    if fmt == 'all':
        zpath = tmpdir / 'chart_bundle.zip'
        with zipfile.ZipFile(zpath, 'w') as z:
            z.write(res['png'], arcname=Path(res['png']).name)
            z.write(res['svg'], arcname=Path(res['svg']).name)
            z.write(res['pptx'], arcname=Path(res['pptx']).name)
        return FileResponse(str(zpath), media_type='application/zip', filename=zpath.name)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
