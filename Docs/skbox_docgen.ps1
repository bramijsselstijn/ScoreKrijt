# Hulpfuncties voor het genereren van de SK-Box-handleidingen (.docx) zonder Word of Python.
# Gebruik: . .\skbox_docgen.ps1 ; Start-Doc ; ... ; Save-Doc -Path ... -HeaderText ... -FooterText ...

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.Drawing

$script:Blue = '214F6B'
$script:Gold = 'C7942E'
$script:Width = 9638
$script:sb = $null
$script:nextNum = 1
$script:numInstances = @()
$script:ShotDir = Join-Path $PSScriptRoot 'Screenshots'
$script:images = @()
$script:shotNr = 0
$script:missingShots = @()

function Start-Doc {
    $script:sb = New-Object System.Text.StringBuilder
    $script:nextNum = 1
    $script:numInstances = @()
    $script:images = @()
    $script:shotNr = 0
}

function Add-Xml([string]$x) { [void]$script:sb.Append($x) }

function Esc([string]$s) { return [System.Security.SecurityElement]::Escape($s) }

function Run([string]$t, [string]$rpr) {
    $pr = ''
    if ($rpr) { $pr = "<w:rPr>$rpr</w:rPr>" }
    return "<w:r>$pr<w:t xml:space='preserve'>$(Esc $t)</w:t></w:r>"
}

# **vet** en `code` binnen lopende tekst
function Inline([string]$text) {
    $o = New-Object System.Text.StringBuilder
    foreach ($part in [regex]::Split($text, '(\*\*.+?\*\*|`[^`]+`)')) {
        if ($part.Length -eq 0) { continue }
        if ($part.StartsWith('**') -and $part.Length -gt 4) {
            [void]$o.Append((Run $part.Substring(2, $part.Length - 4) '<w:b/>'))
        } elseif ($part.StartsWith('`') -and $part.Length -gt 2) {
            [void]$o.Append((Run $part.Substring(1, $part.Length - 2) "<w:rStyle w:val='Inline'/>"))
        } else {
            [void]$o.Append((Run $part ''))
        }
    }
    return $o.ToString()
}

function Para([string]$text, [string]$style, [string]$ppr) {
    $s = ''
    if ($style) { $s = "<w:pStyle w:val='$style'/>" }
    # Een zin die op een dubbele punt eindigt hoort bij het blok eronder.
    if ($text.TrimEnd().EndsWith(':')) { $s += '<w:keepNext/>' }
    Add-Xml "<w:p><w:pPr>$s$ppr</w:pPr>$(Inline $text)</w:p>"
}

function H1([string]$t) { Para $t 'Heading1' }
function H2([string]$t) { Para $t 'Heading2' }
function H3([string]$t) { Para $t 'Heading3' }

function Spacer { Add-Xml "<w:p><w:pPr><w:pStyle w:val='Spacer'/></w:pPr></w:p>" }

function PageBreak { Add-Xml "<w:p><w:r><w:br w:type='page'/></w:r></w:p>" }

function Bullet([string]$t) {
    Para $t 'ListBullet' "<w:numPr><w:ilvl w:val='0'/><w:numId w:val='1'/></w:numPr>"
}

function New-StepList {
    $script:nextNum++
    $script:numInstances += $script:nextNum
    return $script:nextNum
}

function Step([int]$list, [string]$t) {
    Para $t 'ListNumber' "<w:numPr><w:ilvl w:val='0'/><w:numId w:val='$list'/></w:numPr>"
}

function Check([string]$t) {
    Add-Xml ("<w:p><w:pPr><w:pStyle w:val='Check'/></w:pPr>" +
        "<w:r><w:rPr><w:rFonts w:ascii='Segoe UI Symbol' w:hAnsi='Segoe UI Symbol'/><w:color w:val='$script:Blue'/></w:rPr><w:t>$([char]0x2610)</w:t></w:r>" +
        "<w:r><w:tab/></w:r>$(Inline $t)</w:p>")
}

function CodeBlock([string]$code) {
    $lines = @($code.Trim("`r", "`n").Split("`n") | ForEach-Object { $_.TrimEnd("`r") })
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $kn = ''
        if ($i -lt $lines.Count - 1) { $kn = '<w:keepNext/>' }
        Add-Xml "<w:p><w:pPr><w:pStyle w:val='Code'/>$kn</w:pPr><w:r><w:t xml:space='preserve'>$(Esc $lines[$i])</w:t></w:r></w:p>"
    }
    Spacer
}

function Callout([string]$kind, [string]$title, [string]$text) {
    $bar = $script:Blue; $fill = 'EAF1F6'; $ink = $script:Blue
    if ($kind -eq 'warn') { $bar = $script:Gold; $fill = 'FFF6DC'; $ink = '8A5A00' }
    if ($kind -eq 'ok') { $bar = '2E7D5B'; $fill = 'E8F4EE'; $ink = '1F5C42' }
    $w = $script:Width
    Add-Xml ("<w:tbl><w:tblPr><w:tblW w:w='$w' w:type='dxa'/>" +
        "<w:tblBorders><w:left w:val='single' w:sz='36' w:space='0' w:color='$bar'/></w:tblBorders>" +
        "<w:tblLayout w:type='fixed'/>" +
        "<w:tblCellMar><w:top w:w='110' w:type='dxa'/><w:left w:w='200' w:type='dxa'/><w:bottom w:w='110' w:type='dxa'/><w:right w:w='200' w:type='dxa'/></w:tblCellMar>" +
        "</w:tblPr><w:tblGrid><w:gridCol w:w='$w'/></w:tblGrid>" +
        "<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w='$w' w:type='dxa'/><w:shd w:val='clear' w:color='auto' w:fill='$fill'/></w:tcPr>" +
        "<w:p><w:pPr><w:pStyle w:val='TableText'/></w:pPr>$(Run $title "<w:b/><w:color w:val='$ink'/>")$(Run '  ' '')$(Inline $text)</w:p>" +
        "</w:tc></w:tr></w:tbl>")
    Spacer
}

function Tbl([string[]]$headers, [object[]]$rows, [int[]]$widths) {
    $total = ($widths | Measure-Object -Sum).Sum
    $grid = ($widths | ForEach-Object { "<w:gridCol w:w='$_'/>" }) -join ''
    $border = 'w:val="single" w:sz="4" w:space="0" w:color="D5DCE1"'.Replace('"', "'")
    $x = "<w:tbl><w:tblPr><w:tblW w:w='$total' w:type='dxa'/><w:tblBorders>" +
        "<w:top $border/><w:left $border/><w:bottom $border/><w:right $border/><w:insideH $border/><w:insideV $border/>" +
        "</w:tblBorders><w:tblLayout w:type='fixed'/>" +
        "<w:tblCellMar><w:top w:w='70' w:type='dxa'/><w:left w:w='110' w:type='dxa'/><w:bottom w:w='70' w:type='dxa'/><w:right w:w='110' w:type='dxa'/></w:tblCellMar>" +
        "</w:tblPr><w:tblGrid>$grid</w:tblGrid>"
    $x += "<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>"
    for ($c = 0; $c -lt $headers.Count; $c++) {
        $x += "<w:tc><w:tcPr><w:tcW w:w='$($widths[$c])' w:type='dxa'/><w:shd w:val='clear' w:color='auto' w:fill='$script:Blue'/><w:vAlign w:val='center'/></w:tcPr>" +
            "<w:p><w:pPr><w:pStyle w:val='TableText'/></w:pPr>$(Run $headers[$c] '<w:b/><w:color w:val=''FFFFFF''/>')</w:p></w:tc>"
    }
    $x += '</w:tr>'
    for ($r = 0; $r -lt $rows.Count; $r++) {
        $fill = ''
        if ($r % 2 -eq 1) { $fill = "<w:shd w:val='clear' w:color='auto' w:fill='F5F8FA'/>" }
        $x += '<w:tr><w:trPr><w:cantSplit/></w:trPr>'
        for ($c = 0; $c -lt $headers.Count; $c++) {
            $x += "<w:tc><w:tcPr><w:tcW w:w='$($widths[$c])' w:type='dxa'/>$fill<w:vAlign w:val='center'/></w:tcPr>" +
                "<w:p><w:pPr><w:pStyle w:val='TableText'/></w:pPr>$(Inline $rows[$r][$c])</w:p></w:tc>"
        }
        $x += '</w:tr>'
    }
    $x += '</w:tbl>'
    Add-Xml $x
    Spacer
}

# Screenshots: bestanden in Docs\Screenshots (png of jpg, zonder extensie opgegeven).
# Ontbreekt een bestand, dan slaat de build de afbeelding over en meldt dat aan het eind.
function Find-Shot([string]$name) {
    foreach ($ext in '.png', '.jpg', '.jpeg') {
        $p = Join-Path $script:ShotDir ($name + $ext)
        if (Test-Path -LiteralPath $p) { return $p }
    }
    $script:missingShots += $name
    return $null
}

# Leest de afbeelding in, verkleint hem als hij breder is dan 1800 px en geeft de grootte in EMU terug
# (natuurlijke grootte bij 96 dpi, begrensd op $maxW x $maxH).
function Add-ShotImage([string]$path, [long]$maxW, [long]$maxH) {
    $ext = [System.IO.Path]::GetExtension($path).ToLower()
    if ($ext -eq '.jpeg') { $ext = '.jpg' }
    $src = [System.Drawing.Image]::FromFile($path)
    try {
        $w = $src.Width; $h = $src.Height
        $bytes = $null
        if ($w -gt 1800) {
            $nh = [int][math]::Round($h * 1800 / $w)
            $bmp = New-Object System.Drawing.Bitmap(1800, $nh)
            $g = [System.Drawing.Graphics]::FromImage($bmp)
            $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.DrawImage($src, 0, 0, 1800, $nh)
            $g.Dispose()
            $ms = New-Object System.IO.MemoryStream
            if ($ext -eq '.jpg') { $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Jpeg) }
            else { $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png) }
            $bmp.Dispose()
            $bytes = $ms.ToArray()
            $ms.Dispose()
        } else {
            $bytes = [System.IO.File]::ReadAllBytes($path)
        }
        $emuW = [double]$w * 9525; $emuH = [double]$h * 9525
        $scale = [math]::Min(1.0, [math]::Min($maxW / $emuW, $maxH / $emuH))
        $n = $script:images.Count + 1
        $script:images += @{ Rid = "rIdImg$n"; Part = "media/img$n$ext"; Bytes = $bytes }
        return @{ Rid = "rIdImg$n"; Id = 100 + $n; Cx = [long]($emuW * $scale); Cy = [long]($emuH * $scale) }
    } finally { $src.Dispose() }
}

function ImageRun($img, [string]$descr) {
    $rid = $img.Rid; $id = $img.Id; $cx = $img.Cx; $cy = $img.Cy
    return ("<w:r><w:drawing><wp:inline distT='0' distB='0' distL='0' distR='0'>" +
        "<wp:extent cx='$cx' cy='$cy'/><wp:docPr id='$id' name='Afbeelding $id' descr='$(Esc $descr)'/>" +
        "<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect='1'/></wp:cNvGraphicFramePr>" +
        "<a:graphic><a:graphicData uri='http://schemas.openxmlformats.org/drawingml/2006/picture'><pic:pic>" +
        "<pic:nvPicPr><pic:cNvPr id='$id' name='$rid'/><pic:cNvPicPr/></pic:nvPicPr>" +
        "<pic:blipFill><a:blip r:embed='$rid'/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>" +
        "<pic:spPr><a:xfrm><a:off x='0' y='0'/><a:ext cx='$cx' cy='$cy'/></a:xfrm><a:prstGeom prst='rect'><a:avLst/></a:prstGeom>" +
        "<a:ln w='9525'><a:solidFill><a:srgbClr val='B8C2CA'/></a:solidFill></a:ln></pic:spPr>" +
        "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>")
}

function ShotCaption([string]$caption) {
    $script:shotNr++
    return "<w:p><w:pPr><w:pStyle w:val='Caption'/></w:pPr>$(Run ("Afbeelding $($script:shotNr). ") '<w:b/>')$(Inline $caption)</w:p>"
}

# Een afbeelding op de volle breedte (of kleiner als hij van zichzelf klein is), met bijschrift.
function Shot([string]$name, [string]$caption) {
    $path = Find-Shot $name
    if (-not $path) { return }
    $img = Add-ShotImage $path 6120000 4320000
    Add-Xml ("<w:p><w:pPr><w:pStyle w:val='Afbeelding'/><w:keepNext/></w:pPr>$(ImageRun $img $caption)</w:p>" + (ShotCaption $caption))
}

# Twee of drie afbeeldingen naast elkaar, bijvoorbeeld telefoonschermen.
function ShotRow([string[]]$names, [string[]]$captions) {
    $found = @()
    for ($i = 0; $i -lt $names.Count; $i++) {
        $p = Find-Shot $names[$i]
        if ($p) { $found += , @($p, $captions[$i]) }
    }
    if ($found.Count -eq 0) { return }
    $cellW = [int][math]::Floor($script:Width / $found.Count)
    $maxW = [long](($cellW - 200) * 635)
    $grid = ((1..$found.Count) | ForEach-Object { "<w:gridCol w:w='$cellW'/>" }) -join ''
    $x = "<w:tbl><w:tblPr><w:tblW w:w='$($cellW * $found.Count)' w:type='dxa'/><w:tblLayout w:type='fixed'/>" +
        "<w:tblCellMar><w:top w:w='0' w:type='dxa'/><w:left w:w='100' w:type='dxa'/><w:bottom w:w='0' w:type='dxa'/><w:right w:w='100' w:type='dxa'/></w:tblCellMar>" +
        "</w:tblPr><w:tblGrid>$grid</w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr>"
    foreach ($f in $found) {
        $img = Add-ShotImage $f[0] $maxW 4000000
        $x += "<w:tc><w:tcPr><w:tcW w:w='$cellW' w:type='dxa'/></w:tcPr>" +
            "<w:p><w:pPr><w:pStyle w:val='Afbeelding'/><w:keepNext/></w:pPr>$(ImageRun $img $f[1])</w:p>" +
            (ShotCaption $f[1]) + '</w:tc>'
    }
    $x += '</w:tr></w:tbl>'
    Add-Xml $x
    Spacer
}

function Cover([string]$label, [string]$title, [string]$subtitle, [string]$meta, [string]$logoPath) {
    Add-Xml "<w:p><w:pPr><w:spacing w:before='2600' w:after='0'/></w:pPr></w:p>"
    if (Test-Path $logoPath) {
        $e = 1371600
        Add-Xml ("<w:p><w:pPr><w:jc w:val='center'/><w:spacing w:after='360'/></w:pPr><w:r><w:drawing><wp:inline distT='0' distB='0' distL='0' distR='0'>" +
            "<wp:extent cx='$e' cy='$e'/><wp:docPr id='1' name='Logo' descr='ScoreKrijt-logo'/>" +
            "<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect='1'/></wp:cNvGraphicFramePr>" +
            "<a:graphic><a:graphicData uri='http://schemas.openxmlformats.org/drawingml/2006/picture'><pic:pic>" +
            "<pic:nvPicPr><pic:cNvPr id='0' name='logo.png'/><pic:cNvPicPr/></pic:nvPicPr>" +
            "<pic:blipFill><a:blip r:embed='rIdLogo'/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>" +
            "<pic:spPr><a:xfrm><a:off x='0' y='0'/><a:ext cx='$e' cy='$e'/></a:xfrm><a:prstGeom prst='rect'><a:avLst/></a:prstGeom></pic:spPr>" +
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>")
    }
    Para $label 'CoverLabel'
    Para $title 'CoverTitle'
    Para $subtitle 'CoverSubtitle'
    Add-Xml "<w:p><w:pPr><w:pBdr><w:bottom w:val='single' w:sz='12' w:space='1' w:color='$script:Gold'/></w:pBdr><w:spacing w:after='240'/><w:ind w:left='3300' w:right='3300'/></w:pPr></w:p>"
    Para $meta 'CoverMeta'
    Para 'ScoreKrijt en deze handleiding zijn gemaakt met behulp van AI.' 'CoverMeta'
    PageBreak
}

function TocPage {
    Para 'Inhoud' 'TOCHeading'
    Add-Xml ("<w:p><w:r><w:fldChar w:fldCharType='begin'/></w:r><w:r><w:instrText xml:space='preserve'> TOC \o ""1-2"" \h \z \u </w:instrText></w:r>" +
        "<w:r><w:fldChar w:fldCharType='separate'/></w:r><w:r><w:t>Inhoudsopgave wordt bijgewerkt bij het openen.</w:t></w:r><w:r><w:fldChar w:fldCharType='end'/></w:r></w:p>")
    PageBreak
}

function Get-StylesXml {
    $f = "<w:rFonts w:ascii='Calibri' w:hAnsi='Calibri' w:cs='Calibri' w:eastAsia='Calibri'/>"
    return @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>$f<w:color w:val="21272B"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="nl-NL" w:eastAsia="nl-NL" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="288" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>
<w:pPr><w:keepNext/><w:keepLines/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="$script:Gold"/></w:pBdr><w:spacing w:before="480" w:after="180"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:color w:val="$script:Blue"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/>
<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="320" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:b/><w:color w:val="$script:Blue"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/>
<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="220" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr>
<w:rPr><w:b/><w:color w:val="1F4D78"/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverLabel"><w:name w:val="Cover label"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="160"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:color w:val="$script:Gold"/><w:spacing w:val="40"/><w:sz w:val="21"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverTitle"><w:name w:val="Cover titel"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="160" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:color w:val="$script:Blue"/><w:sz w:val="68"/><w:szCs w:val="68"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverSubtitle"><w:name w:val="Cover ondertitel"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="360"/><w:ind w:left="1200" w:right="1200"/><w:jc w:val="center"/></w:pPr><w:rPr><w:color w:val="5F6970"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverMeta"><w:name w:val="Cover gegevens"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:color w:val="5F6970"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="TOCHeading"><w:name w:val="Inhoud kop"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="$script:Gold"/></w:pBdr><w:spacing w:before="0" w:after="240"/></w:pPr><w:rPr><w:b/><w:color w:val="$script:Blue"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9638"/></w:tabs><w:spacing w:before="140" w:after="40"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9638"/></w:tabs><w:spacing w:after="20"/><w:ind w:left="300"/></w:pPr><w:rPr><w:color w:val="404B52"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="Code"><w:name w:val="Opdracht"/><w:basedOn w:val="Normal"/><w:qFormat/>
<w:pPr><w:keepLines/><w:pBdr><w:top w:val="single" w:sz="4" w:space="5" w:color="1F2A33"/><w:left w:val="single" w:sz="4" w:space="8" w:color="1F2A33"/><w:bottom w:val="single" w:sz="4" w:space="5" w:color="1F2A33"/><w:right w:val="single" w:sz="4" w:space="8" w:color="1F2A33"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="1F2A33"/><w:spacing w:before="0" w:after="0" w:line="264" w:lineRule="auto"/><w:ind w:left="200" w:right="200"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:color w:val="E8EEF2"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
<w:style w:type="character" w:customStyle="1" w:styleId="Inline"><w:name w:val="Opdracht in tekst"/><w:uiPriority w:val="1"/><w:qFormat/><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:color w:val="214F6B"/><w:sz w:val="19"/><w:szCs w:val="19"/><w:shd w:val="clear" w:color="auto" w:fill="EEF2F5"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="TableText"><w:name w:val="Tabeltekst"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="0" w:line="264" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="Spacer"><w:name w:val="Tussenruimte"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="exact"/></w:pPr><w:rPr><w:sz w:val="12"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:qFormat/><w:pPr><w:spacing w:after="60"/><w:ind w:left="454" w:hanging="284"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="ListNumber"><w:name w:val="List Number"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:qFormat/><w:pPr><w:spacing w:after="80"/><w:ind w:left="454" w:hanging="340"/></w:pPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="Check"><w:name w:val="Controlepunt"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="60"/><w:ind w:left="454" w:hanging="454"/></w:pPr></w:style>
<w:style w:type="paragraph" w:customStyle="1" w:styleId="Afbeelding"><w:name w:val="Afbeelding"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="35"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="200" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr><w:rPr><w:i/><w:color w:val="5F6970"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" w:color="D5DCE1"/></w:pBdr><w:tabs><w:tab w:val="right" w:pos="9638"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:b/><w:color w:val="6B767F"/><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="99"/><w:pPr><w:tabs><w:tab w:val="right" w:pos="9638"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:color w:val="6B767F"/><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr></w:style>
</w:styles>
"@
}

function Get-NumberingXml {
    $x = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="454" w:hanging="284"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="$script:Gold"/></w:rPr></w:lvl></w:abstractNum>
<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="454" w:hanging="340"/></w:pPr><w:rPr><w:b/><w:color w:val="$script:Blue"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
"@
    foreach ($n in $script:numInstances) {
        $x += "<w:num w:numId=""$n""><w:abstractNumId w:val=""1""/><w:lvlOverride w:ilvl=""0""><w:startOverride w:val=""1""/></w:lvlOverride></w:num>`n"
    }
    return $x + '</w:numbering>'
}

function Save-Doc([string]$Path, [string]$HeaderText, [string]$FooterText, [string]$LogoPath, [string]$Title) {
    $ns = "xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships'"
    $nsDoc = "$ns xmlns:wp='http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing' xmlns:a='http://schemas.openxmlformats.org/drawingml/2006/main' xmlns:pic='http://schemas.openxmlformats.org/drawingml/2006/picture'"
    $decl = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + "`n"

    $sect = "<w:sectPr><w:headerReference w:type='default' r:id='rIdHeader'/><w:footerReference w:type='default' r:id='rIdFooter'/>" +
        "<w:pgSz w:w='11906' w:h='16838'/><w:pgMar w:top='1304' w:right='1134' w:bottom='1134' w:left='1134' w:header='567' w:footer='510' w:gutter='0'/><w:titlePg/></w:sectPr>"
    $document = $decl + "<w:document $nsDoc><w:body>" + $script:sb.ToString() + $sect + '</w:body></w:document>'

    $header = $decl + "<w:hdr $ns><w:p><w:pPr><w:pStyle w:val='Header'/></w:pPr><w:r><w:t>$(Esc $HeaderText)</w:t></w:r></w:p></w:hdr>"
    $footer = $decl + "<w:ftr $ns><w:p><w:pPr><w:pStyle w:val='Footer'/></w:pPr><w:r><w:t>$(Esc $FooterText)</w:t></w:r><w:r><w:tab/></w:r>" +
        "<w:r><w:t xml:space='preserve'>Pagina </w:t></w:r><w:fldSimple w:instr=' PAGE '><w:r><w:t>1</w:t></w:r></w:fldSimple>" +
        "<w:r><w:t xml:space='preserve'> van </w:t></w:r><w:fldSimple w:instr=' NUMPAGES '><w:r><w:t>1</w:t></w:r></w:fldSimple></w:p></w:ftr>"

    $settings = $decl + "<w:settings $ns><w:zoom w:percent='100'/><w:defaultTabStop w:val='709'/><w:characterSpacingControl w:val='doNotCompress'/>" +
        "<w:compat><w:compatSetting w:name='compatibilityMode' w:uri='http://schemas.microsoft.com/office/word' w:val='15'/></w:compat></w:settings>"

    $contentTypes = $decl + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
        '<Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="jpg" ContentType="image/jpeg"/>' +
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>' +
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>' +
        '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>' +
        '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>' +
        '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>' +
        '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>' +
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>' +
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'

    $rels = $decl + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>' +
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>' +
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'

    $docRels = $decl + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
        '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' +
        '<Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>' +
        '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>' +
        '<Relationship Id="rIdHeader" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>' +
        '<Relationship Id="rIdFooter" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>' +
        '<Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo.png"/>'
    foreach ($im in $script:images) {
        $docRels += "<Relationship Id=""$($im.Rid)"" Type=""http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"" Target=""$($im.Part)""/>"
    }
    $docRels += '</Relationships>'

    $stamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $core = $decl + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' +
        "<dc:title>$(Esc $Title)</dc:title><dc:creator>ScoreKrijt</dc:creator><dc:language>nl-NL</dc:language>" +
        "<dcterms:created xsi:type=""dcterms:W3CDTF"">$stamp</dcterms:created><dcterms:modified xsi:type=""dcterms:W3CDTF"">$stamp</dcterms:modified></cp:coreProperties>"
    $app = $decl + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Office Word</Application></Properties>'

    $parts = [ordered]@{
        '[Content_Types].xml'          = $contentTypes
        '_rels/.rels'                  = $rels
        'word/document.xml'            = $document
        'word/_rels/document.xml.rels' = $docRels
        'word/styles.xml'              = (Get-StylesXml)
        'word/numbering.xml'           = (Get-NumberingXml)
        'word/settings.xml'            = $settings
        'word/header1.xml'             = $header
        'word/footer1.xml'             = $footer
        'docProps/core.xml'            = $core
        'docProps/app.xml'             = $app
    }

    if (Test-Path $Path) { Remove-Item $Path -Force }
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    $zip = [System.IO.Compression.ZipFile]::Open($Path, 'Create')
    try {
        foreach ($name in $parts.Keys) {
            $entry = $zip.CreateEntry($name)
            $bytes = $utf8.GetBytes($parts[$name])
            $s = $entry.Open(); $s.Write($bytes, 0, $bytes.Length); $s.Close()
        }
        if (Test-Path $LogoPath) {
            $entry = $zip.CreateEntry('word/media/logo.png')
            $bytes = [System.IO.File]::ReadAllBytes($LogoPath)
            $s = $entry.Open(); $s.Write($bytes, 0, $bytes.Length); $s.Close()
        }
        foreach ($im in $script:images) {
            $entry = $zip.CreateEntry('word/' + $im.Part)
            $s = $entry.Open(); $s.Write($im.Bytes, 0, $im.Bytes.Length); $s.Close()
        }
    } finally { $zip.Dispose() }
}

# Opent het document in Word, werkt de inhoudsopgave bij, slaat op en exporteert een pdf.
function Update-InWord([string]$DocPath, [string]$PdfPath) {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    try {
        $doc = $word.Documents.Open($DocPath)
        if ($doc.TablesOfContents.Count -gt 0) { $doc.TablesOfContents.Item(1).Update() }
        $doc.Fields.Update() | Out-Null
        $doc.Save()
        $doc.ExportAsFixedFormat($PdfPath, 17)
        $pages = $doc.ComputeStatistics(2)
        $doc.Close(0)
        return $pages
    } finally { $word.Quit() }
}
