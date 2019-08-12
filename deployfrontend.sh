rsync -r src/ docs/
rsync build/contracts/ArchiveCertification.json docs/
git add .
git commit -m "adding fronted files to Github pages"
git push
