const path = require('path');
const fs = require('fs');

const outputPath = path.join(__dirname, '../output.json');

function lerOutput() {
  if (!fs.existsSync(outputPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
  } catch {
    return null;
  }
}

exports.getMockPapers = (req, res) => {
  const data = lerOutput();
  if (!data || !Array.isArray(data.citations)) {
    return res.status(404).json({ error: 'Citações não encontradas no output.json' });
  }

  // Retorna só o array de citações
  res.json(data.citations);
};

// Função que busca artigo por DOI
exports.searchByDOI = (req, res) => {
  const { doi } = req.query;

  if (!doi) {
    return res.status(400).json({ error: 'DOI não fornecido' });
  }

  const data = lerOutput();
  if (!data || !data.input_doi || data.input_doi !== doi) {
    return res.status(404).json({ error: 'Artigo não encontrado com esse DOI' });
  }

  res.json(data);
};

// Marcar artigo com "incluir", "excluir", "talvez"
exports.marcarArtigo = (req, res) => {
  const { paperId, status } = req.body;

  if (!paperId || !status) {
    return res.status(400).json({ error: 'paperId e status são obrigatórios' });
  }

  const data = lerOutput();
  if (!data || !Array.isArray(data.citations)) {
    return res.status(500).json({ error: 'Erro ao carregar as citações' });
  }

  const artigo = data.citations.find(a => a.paperId === paperId);
  if (!artigo) {
    return res.status(404).json({ error: 'Artigo não encontrado' });
  }

  artigo.selecionado = status;

  try {
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), 'utf-8');
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao salvar o status' });
  }
};

// Retorna apenas os artigos marcados como "incluir"
exports.getArtigosIncluidos = (req, res) => {
  const data = lerOutput();
  if (!data || !Array.isArray(data.citations)) {
    return res.status(500).json({ error: 'Erro ao carregar as citações' });
  }

  const incluidos = data.citations.filter(a => a.selecionado === 'incluir');
  res.json(incluidos);
};
