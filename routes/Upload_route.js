const express = require("express");
const fs = require("fs");
const router = express.Router();
const multer = require("multer");
const { spawn } = require("child_process");
const path = require("path");

// Use process.cwd() for reliable root directory access in production
const root_dir = process.cwd();

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = path.join(root_dir, "uploaded");
        if (!fs.existsSync(uploadPath)) fs.mkdirSync(uploadPath);
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + "-" + file.originalname);
    },
});

const upload = multer({ storage: storage });

router.post("/upload", upload.single("file"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    const { template, method } = req.body;
    const filePath = req.file.path;

    // Map template value to index (template1 -> 0, template2 -> 1, etc.)
    const templateIdx = template ? template.replace("template", "") - 1 : 0;

    // Logic for Method selection
    let scriptPath;
    if (method === "LLM-API") {
        scriptPath = path.join(
            root_dir,
            "routes",
            "CV_Process",
            "LLM_Pipeline",
            "LLM_1.py",
        );
    } else {
        scriptPath = path.join(
            root_dir,
            "routes",
            "CV_Process",
            "NLP_Pipeline",
            "NLP_1.py",
        );
    }

    // Spawn Python with file path AND template index
    const pythonProcess = spawn("python", [scriptPath, filePath, templateIdx]);

    let output_path = "";
    pythonProcess.stdout.on("data", (data) => {
        output_path += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        // Clean up uploaded file
        fs.unlink(filePath, (err) => {
            if (err) console.error(`Cleanup Error: ${err}`);
        });

        if (code !== 0 || !output_path.trim()) {
            return res.status(500).send("Processing failed. Check server logs.");
        }

        const finalPath = output_path.trim();
        const fileName = path.basename(finalPath);

        res.render("result", {
            outputPath: finalPath, // Absolute path for logging/debugging
            fileName: fileName, // Used for the 'download' attribute
            downloadUrl: `/portfolios/${fileName}`, // The URL the browser uses
            method: req.body.method, // To show which pipeline was used
        });
    });
});

module.exports = router;
