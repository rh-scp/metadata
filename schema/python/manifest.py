import jsl, json
# vim: set fileencoding=utf-8
# Pavel Odvody <podvody@redhat.com>
#
# Common Metadata Interchange Format - Python Model
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307 USA


""" Well qualified name pattern """
NAME_PATTERN='^[A-Za-z0-9_\-\.]*$'

class Version(jsl.Document):
        """ X.Y.Z version specification

        components are called <MAJOR>.<MINOR>.<BUILD>
        """
        class Options(object):
                definition_id = 'version'

        major = jsl.NumberField(minimum=0, maximum=999, required=True, description='major version number')
        minor = jsl.NumberField(minimum=0, maximum=999, description='minor version number')
        build = jsl.NumberField(minimum=0, maximum=999, description='build version number')

class VersionRange(jsl.Document):
        """ Version range specification

        allows specifying both exclusive/inclusive version ranges/sets
        """
        class Options(object):
                definition_id = 'version-range'

        version_start = jsl.DocumentField(Version, as_ref=True, required=True, description='version range start')
        version_end = jsl.DocumentField(Version, as_ref=True, required=True, description='version range end')
        start_exclusive = jsl.BooleanField(description='make the start specification exclusive')
        end_exclusive = jsl.BooleanField(description='make the end specification exclusive')

class AbstractDependency(jsl.Document):
        """ Base class for dependencies

        each dependency has name and source URI
        """
        class Options(object):
                definition_id = 'abstract-dependency'

        type = jsl.StringField(enum=['abstract-dependency'])
        name = jsl.StringField(required=True, description='name of the dependency')
        source = jsl.UriField(description='URI source of the dependency')

class RangeDependency(AbstractDependency):
        """ Version range dependency

        """
        class Options(object):
                definition_id = 'range-dependency'

        type = jsl.StringField(enum=['range-dependency'])
        range = jsl.DocumentField(VersionRange, as_ref=True, required=True, description='version range dependency')

class VersionDependency(AbstractDependency):
        """ Exact version dependency

        """
        class Options(object):
                definition_id = 'version-dependency'

        type = jsl.StringField(enum=['varsion-dependency'])
        version = jsl.DocumentField(Version, as_ref=True, required=True, description='exact version dependency')

class NotVersionDependency(AbstractDependency):
        """ Negates the result of another `AbstractDependency`

        """
        class Options(object):
                definition_id = 'not-version-dependency'

        type = jsl.StringField(enum=['not-version-dependency'])
        target = jsl.DocumentField(AbstractDependency, as_ref=True, required=True, description='version specificaiton to negate')

class AndDependencyGroup(AbstractDependency):
        """ Collates `items` under `AND` clause

        """
        class Options(object):
                definition_id = 'and-version-dependency'

        type = jsl.StringField(enum=['and-version-dependency'])
        items = jsl.ArrayField(jsl.DocumentField(AbstractDependency, as_ref=True),
                  required=True, description='items to join with AND')

class OrDependencyGroup(AbstractDependency):
        """ Collates `items` under `OR` clause

        """
        class Options(object):
                definition_id = 'or-version-dependency'

        type = jsl.StringField(enum=['or-version-dependency'])
        items = jsl.ArrayField(jsl.DocumentField(AbstractDependency, as_ref=True),
                  required=True, description='items to join with OR')

class FileTrait(jsl.Document):
        """ Describes basic properties of file provides

        """
        class Options(object):
                definition_id = 'file-trait'

        is_executable = jsl.BooleanField(description='true for executable binaries')
        is_library = jsl.BooleanField(description='true for library binaries')
        is_header = jsl.BooleanField(description='true for header files')
        is_source = jsl.BooleanField(description='true for source files')
        language = jsl.StringField(description='implementation language', required=True)

class FileProvides(jsl.Document):
        """ Each file should corresopond to exactly one provide

        """
        class Options(object):
                definition_id = 'file-provide'

        name = jsl.StringField(description='basename of the file')
        uri = jsl.StringField(format='uri', description='chroot relative uri of the file')
        hash = jsl.StringField(pattern='^[A-Fa-f0-9]{32}$', description='sha256 digest of the file')
        architecture = jsl.StringField(pattern=NAME_PATTERN, description='architecture description string')
        traits = jsl.ArrayField(
                   jsl.DocumentField(FileTrait, as_ref=True),
                   description='traits of the file')

class Archive(jsl.Document):
        """ Describes a source archives

        """
        class Options(object):
                definition_id = 'archive'

        uri = jsl.UriField(description='location of the archive')
        hash = jsl.StringField(pattern='^[A-Fa-f0-9]{32}$', description='sha256 digest of the archive')


class Manifest(jsl.Document):
        """ Manifest 

        """
        class Options(object):
                definition_id = 'manifest'

        artifact_version = jsl.DocumentField(Version, as_ref=True, required=True)
        manifest_version = jsl.DocumentField(Version, as_ref=True, required=True)
        sources = jsl.ArrayField(jsl.DocumentField(Archive, as_ref=True), description='all source archives for the artifact')
        origin = jsl.UriField(description='authoritative source of the artifact')
        name = jsl.StringField(pattern=NAME_PATTERN, required=True, description='name of the artifact')
        licenses = jsl.ArrayField(jsl.StringField(), description='licenses applicable to the artifact')
        dependencies = jsl.ArrayField([jsl.DocumentField(AbstractDependency, as_ref=True), 
                                   jsl.DocumentField(RangeDependency, as_ref=True),
                                   jsl.DocumentField(VersionDependency, as_ref=True),
                                   jsl.DocumentField(NotVersionDependency, as_ref=True),
                                   jsl.DocumentField(AndDependencyGroup, as_ref=True),
                                   jsl.DocumentField(OrDependencyGroup, as_ref=True)],
                        unique_items=True, description='list of artifact dependencies')
        provides = jsl.ArrayField(jsl.DocumentField(FileProvides, as_ref=True),
                                description='list of provided files')

print(json.dumps(Manifest().get_schema()))
