FIGURE = document.getElementById('figure')


// var trace1 = {
//
// 	x:[1, 2, 3], y: [1, 2, 3], z: [1, 2, 3],
// 	mode: 'markers',
// 	marker: {
//
// 	type: 'scatter3d'
// };

function coneArray(H, R, xPoints=20, tPoints=20, rPoints=5) {
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
                let hsv = [theta, r / R, z / H]

                xs.push(x)
                ys.push(y)
                zs.push(z)
                colours.push(hsv)
            }
        }
    }
    return [xs, ys, zs, colours]
}

function getTrace(H, R) {
    let [x, y, z, hsv] = coneArray(H, R);
    let trace = {
        x: x, y: y, z: z,
        mode: "markers",
        marker: {
            size: 12,
            line: {
                color: 'rgba(217, 217, 217, 0.14)'
            },
            opacity: 0.4
            },
        type: "scatter3d"
        };
    return trace
}

let trace = getTrace(100, 100)
Plotly.newPlot(FIGURE, [trace]);