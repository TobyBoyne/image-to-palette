FIGURE = document.getElementById('figure')

const HUE_MAX = 2 * Math.PI
const SV_MAX = 1
const RGB_MAX = 255

function coneArray(H, R, xPoints=20, tPoints=50, rPoints=5) {
    let xs = []
    let ys = []
    let zs = []
    let colours = []


    for (let i=0; i<xPoints; i++){
        let z = i * H / xPoints
        let v = (H - z) / H
        for (let j=0; j<tPoints; j++){
            let theta = j * Math.PI * 2 / tPoints
            for (let k=0; k<rPoints; k++){
                let r = R * k / rPoints
                let x = r * v * Math.cos(theta)
                let y = r * v * Math.sin(theta)
                let colour = hsv2Rgb(theta, r / R, z / H)
                xs.push(x)
                ys.push(y)
                zs.push(z)
                colours.push(colour)
            }
        }
    }
    return [xs, ys, zs, colours]
}

function getTrace(H, R) {
    let [x, y, z, colours] = coneArray(H, R);
    console.log(colours)
    let trace = {
        x: x, y: y, z: z,
        mode: "markers",
        marker: {
            size: 12,
            color: colours,
            opacity: 0.2
            },
        type: "scatter3d"
        };
    return trace
}

hsv2Rgb = function (h, s, v) {
    h = (h === HUE_MAX) ? 1 : (h % HUE_MAX / parseFloat(HUE_MAX) * 6)
    s = (s === SV_MAX) ? 1 : (s % SV_MAX / parseFloat(SV_MAX))
    v = (v === SV_MAX) ? 1 : (v % SV_MAX / parseFloat(SV_MAX))
    var i = Math.floor(h)
    var f = h - i
    var p = v * (1 - s)
    var q = v * (1 - f * s)
    var t = v * (1 - (1 - f) * s)
    var mod = i % 6
    var r = [v, q, p, p, t, v][mod]
    var g = [t, v, v, q, p, p][mod]
    var b = [p, p, t, v, v, q][mod]

    //convert rgb to hex format
    r = Math.round(r * RGB_MAX)
    g = Math.round(g * RGB_MAX)
    b = Math.round(b * RGB_MAX)
    let hex = "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    return hex
}

let trace = getTrace(100, 100)


Plotly.newPlot(FIGURE, [trace]);