FIGURE = document.getElementById('figure')

// TODO: Show solid cone on left plot, then points on right plot
// left and right plots should have matching camera angle



const HUE_MAX = 2 * Math.PI
const SV_MAX = 1
const RGB_MAX = 255

const H = 100,
    R = 100;

function coneArray(xPoints=20, tPoints=50, rPoints=5) {
    let xs = []
    let ys = []
    let zs = []
    let colours = []


    for (let i=0; i<xPoints; i++){
        let z = i * H / xPoints
        let v = -z / H
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

function coneMesh(numPoints=20){
    let xs = [0, 0]
    let ys = [0, 0]
    let zs = [0, H]
    let colours = ["#000000", "#FFFFFF"]

    for (let i=0; i<numPoints; i++){
        let theta = i * Math.PI * 2 / numPoints
        let x_ = R * Math.cos(theta)
        let y_ = R * Math.sin(theta)
        let z_ = H
        let colour_ = hsv2Rgb(theta, 1, 1)

        xs.push(x_)
        ys.push(y_)
        zs.push(z_)
        colours.push(colour_)
    }

    // i, j, k refer to triangles that make up mesh
    // each triangle points to two adjecent points on the ring of the cone, then either
    //  the origin (0) or the centre of the top face (1)

    let is = []
    let js = []
    let ks = []

    for (let idx1=2; idx1<numPoints+2; idx1++){
        let idx2 = idx1 !== numPoints+1 ? idx1+1 : 2
        let i_ = [idx1, idx1]
        let j_ = [idx2, idx2]
        let k_ = [0, 1]

        is.push(...i_)
        js.push(...j_)
        ks.push(...k_)
    }

    let data = [{
        type: "mesh3d",
        x: xs,
        y: ys,
        z: zs,
        i: is,
        j: js,
        k: ks,
        vertexcolor: colours
    }];
    return data
}

function getTrace(xs, ys, zs, colours, options) {
    // let [x, y, z, colours] = coneArray();
    console.log(colours)
    let trace = {
        x: xs, y: ys, z: zs,
        mode: "markers",
        marker: {
            size: 12,
            color: colours,
            opacity: options.opacity ? options.opacity : 0.5
            },
        type: "scatter3d"
        };
    return trace
}


function getRandomPoints(numPoints) {
//  Gets a number of random points
    let xs = []
    let ys = []
    let zs = []
    let colours = []

    for (let i=0; i<numPoints; i++) {
        let theta = 2 * Math.PI * Math.random()
        let z = H * Math.random()
        let r = R * Math.random()
        let v = -z / H

        xs.push(r * v * Math.cos(theta))
        ys.push(r * v * Math.sin(theta))
        zs.push(z)
        colours.push(hsv2Rgb(theta, r / R, z / H))
    }

    return [xs, ys, zs, colours]
}

function hsv2Rgb (h, s, v) {
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
// let trace = getTrace()
// Plotly.newPlot(FIGURE, [trace]);

// let [xs, ys, zs, colours] = getRandomPoints(10)
// let randTrace = getTrace(xs, ys, zs, colours, 1)
// // let [xs1, ys1, zs1, colours1] = coneArray()
// // let coneTrace = getTrace(xs1, ys1, zs1, colours1, 0.1)
// Plotly.newPlot(FIGURE, [randTrace])

let x = {a: 'b', c: 'd'}
console.log(x.a ? x.a : 2)

let data = coneMesh(50)
Plotly.newPlot(FIGURE, data)
