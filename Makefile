#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

.NOTPARALLEL:

export PYTHONPATH := python

.PHONY: serve
serve:
	python3 -m transom render --verbose --force --serve 8080 config input docs

.PHONY: render
render:
	python3 -m transom render --verbose config input docs

.PHONY: force-render
force-render:
	python3 -m transom render --force --verbose config input docs

.PHONY: check-links
check-links:
	python3 -m transom check-links --verbose config input docs

.PHONY: check-files
check-files:
	python3 -m transom check-files --verbose config input docs

.PHONY: clean
clean:
	rm -rf python/__pycache__

.PHONY: update-transom
update-transom:
	curl -sfo python/markdown2.py "https://raw.githubusercontent.com/ssorj/transom/master/python/markdown2.py"
	curl -sfo python/transom.py "https://raw.githubusercontent.com/ssorj/transom/master/python/transom.py"

.PHONY: update-%
update-%:
	curl -sfo python/$*.py "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py"


.PHONY: didact
didact:
	cp input/start/index.md skupper.didact.md
	hygen didact readme
